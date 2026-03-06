#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
燕云十六声 - 装备批量扫描工具
燕云装备助手配套工具 - 自动 OCR 识别背包装备并导出 JSON

功能:
- 批量截图背包装备列表
- OCR 识别装备信息（名称、品质、词条、强化等级）
- 自动生成网站兼容的 JSON 文件
- 支持手动导入截图批量处理

作者：燕云装备助手
版本：v1.0
日期：2026-03-06
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 第三方库
try:
    import pyautogui
    from PIL import Image
    import pygetwindow as gw
    import keyboard
    import pytesseract
    import cv2
    import numpy as np
except ImportError as e:
    print(f"❌ 缺少依赖库：{e}")
    print("请运行：pip install -r requirements_scanner.txt")
    sys.exit(1)

# 配置
CONFIG_FILE = "scanner_config.json"
DEFAULT_CONFIG = {
    "game_window_title": "燕云十六声",
    "output_dir": "scans",
    "json_output": "equipment_export.json",
    "ocr_lang": "chi_sim+eng",
    "capture_delay": 2,  # 截图间隔（秒）
    "image_format": "png",
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scanner.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EquipmentScanner:
    """装备批量扫描工具类"""
    
    def __init__(self, config=None):
        """初始化工具"""
        self.config = config or self.load_config()
        self.output_dir = Path(self.config["output_dir"])
        self.output_dir.mkdir(exist_ok=True)
        self.scanned_equipment = []
        self.game_window = None
        
        # 配置 pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # 配置 pytesseract
        # Windows 用户需要安装 Tesseract-OCR 并配置路径
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        logger.info("✅ 装备扫描工具初始化完成")
        logger.info(f"📁 输出目录：{self.output_dir.absolute()}")
    
    def load_config(self):
        """加载配置文件"""
        if Path(CONFIG_FILE).exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**DEFAULT_CONFIG, **config}
            except Exception as e:
                logger.warning(f"配置文件加载失败：{e}，使用默认配置")
        return DEFAULT_CONFIG
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info("✅ 配置已保存")
        except Exception as e:
            logger.error(f"❌ 保存配置失败：{e}")
    
    def find_game_window(self):
        """查找游戏窗口"""
        title = self.config["game_window_title"]
        logger.info(f"🔍 正在查找游戏窗口：{title}")
        
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                self.game_window = windows[0]
                logger.info(f"✅ 找到游戏窗口：{self.game_window.title}")
                return True
            else:
                logger.warning(f"⚠️ 未找到游戏窗口，请确保游戏已启动")
                return False
        except Exception as e:
            logger.error(f"❌ 查找窗口失败：{e}")
            return False
    
    def capture_equipment_list(self, region=None):
        """截取装备列表"""
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                # 截取整个游戏窗口
                if not self.game_window:
                    if not self.find_game_window():
                        return None
                
                self.game_window.activate()
                time.sleep(0.5)
                
                region = (
                    self.game_window.left,
                    self.game_window.top,
                    self.game_window.width,
                    self.game_window.height
                )
                screenshot = pyautogui.screenshot(region=region)
            
            # 保存截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / f"equip_list_{timestamp}.{self.config['image_format']}"
            
            if self.config["image_format"].upper() == "PNG":
                screenshot.save(filepath, "PNG", optimize=True)
            else:
                screenshot.save(filepath, quality=95)
            
            logger.info(f"✅ 装备列表截图已保存：{filepath}")
            return filepath, screenshot
        except Exception as e:
            logger.error(f"❌ 截图失败：{e}")
            return None, None
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """图像预处理（增强 OCR 识别率）"""
        # 转换为 OpenCV 格式
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # 转换为灰度图
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 二值化（增强对比度）
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 降噪
        denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
        
        return denoised
    
    def ocr_recognition(self, image: Image.Image) -> str:
        """OCR 识别"""
        try:
            # 预处理图像
            processed_img = self.preprocess_image(image)
            
            # OCR 识别
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                processed_img,
                lang=self.config["ocr_lang"],
                config=custom_config
            )
            
            return text.strip()
        except Exception as e:
            logger.error(f"❌ OCR 识别失败：{e}")
            return ""
    
    def parse_equipment_info(self, ocr_text: str) -> Dict[str, Any]:
        """解析 OCR 识别结果"""
        equipment = {
            "name": "",
            "quality": 3,
            "level": 0,
            "set_name": "",
            "stats": [],
            "raw_text": ocr_text,
        }
        
        try:
            lines = ocr_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 识别装备名称（第一行）
                if not equipment["name"]:
                    equipment["name"] = line
                    continue
                
                # 识别品质（星级）
                if '⭐' in line or '★' in line:
                    star_count = line.count('⭐') + line.count('★')
                    if star_count > 0:
                        equipment["quality"] = min(star_count, 5)
                
                # 识别强化等级
                if '+' in line:
                    import re
                    match = re.search(r'\+(\d+)', line)
                    if match:
                        equipment["level"] = int(match.group(1))
                
                # 识别词条
                if any(keyword in line for keyword in ['外功', '精准', '会心', '攻击', '防御']):
                    equipment["stats"].append({
                        "type": "unknown",
                        "value": line,
                        "raw": line
                    })
            
            logger.info(f"📝 解析装备信息：{equipment['name']} (品质:{equipment['quality']}, 强化:+{equipment['level']})")
            
        except Exception as e:
            logger.error(f"❌ 解析 OCR 结果失败：{e}")
        
        return equipment
    
    def scan_and_recognize(self) -> List[Dict[str, Any]]:
        """扫描并识别装备列表"""
        logger.info("🔍 开始扫描装备列表...")
        
        # 截图
        filepath, screenshot = self.capture_equipment_list()
        if not screenshot:
            return []
        
        # OCR 识别
        ocr_text = self.ocr_recognition(screenshot)
        if not ocr_text:
            logger.warning("⚠️ OCR 识别结果为空")
            return []
        
        # 解析装备信息
        equipment = self.parse_equipment_info(ocr_text)
        equipment["image_path"] = str(filepath)
        equipment["scan_time"] = datetime.now().isoformat()
        
        self.scanned_equipment.append(equipment)
        
        return self.scanned_equipment
    
    def export_to_json(self, filename=None):
        """导出为 JSON 文件"""
        try:
            if not filename:
                filename = self.config["json_output"]
            
            filepath = self.output_dir / filename
            
            # 生成网站兼容的格式
            export_data = {
                "version": "1.0",
                "export_time": datetime.now().isoformat(),
                "tool": "燕云装备助手 - 批量扫描工具",
                "equipment_count": len(self.scanned_equipment),
                "equipment_list": self.scanned_equipment
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 已导出 {len(self.scanned_equipment)} 件装备到：{filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ 导出 JSON 失败：{e}")
            return None
    
    def import_images(self, image_folder=None):
        """从文件夹导入截图批量处理"""
        try:
            if not image_folder:
                image_folder = self.output_dir
            
            folder_path = Path(image_folder)
            image_files = list(folder_path.glob("*.png")) + list(folder_path.glob("*.jpg"))
            
            logger.info(f"📁 找到 {len(image_files)} 张截图")
            
            for image_file in image_files:
                logger.info(f"🔍 处理：{image_file.name}")
                
                try:
                    image = Image.open(image_file)
                    ocr_text = self.ocr_recognition(image)
                    
                    if ocr_text:
                        equipment = self.parse_equipment_info(ocr_text)
                        equipment["image_path"] = str(image_file)
                        equipment["scan_time"] = datetime.now().isoformat()
                        self.scanned_equipment.append(equipment)
                    
                    time.sleep(0.5)  # 避免处理过快
                except Exception as e:
                    logger.error(f"❌ 处理 {image_file.name} 失败：{e}")
            
            logger.info(f"✅ 批量处理完成，共识别 {len(self.scanned_equipment)} 件装备")
            return self.scanned_equipment
        except Exception as e:
            logger.error(f"❌ 批量导入失败：{e}")
            return []
    
    def start(self):
        """启动工具"""
        print("\n" + "=" * 50)
        print("🎮 燕云十六声 - 装备批量扫描工具")
        print("=" * 50)
        print(f"📁 输出目录：{self.output_dir.absolute()}")
        print(f"📝 JSON 输出：{self.config['json_output']}")
        print("=" * 50)
        print("\n💡 使用说明:")
        print("  1. 启动游戏，打开背包/装备界面")
        print("  2. 按 F10 开始扫描当前装备列表")
        print("  3. 按 F11 从文件夹导入截图批量处理")
        print("  4. 按 F12 导出 JSON 文件")
        print("  5. 鼠标移到屏幕左上角可紧急停止")
        print("  6. 按 Ctrl+C 退出程序")
        print("-" * 50)
        
        # 查找游戏窗口
        self.find_game_window()
        
        # 注册热键
        keyboard.add_hotkey('f10', lambda: self.scan_and_recognize())
        keyboard.add_hotkey('f11', lambda: self.import_images())
        keyboard.add_hotkey('f12', lambda: self.export_to_json())
        
        logger.info("✅ 热键已注册：F10 扫描 | F11 导入 | F12 导出")
        
        # 主循环
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            logger.info("👋 正在退出...")
        finally:
            # 自动导出
            if self.scanned_equipment:
                self.export_to_json()
            keyboard.remove_all_hotkeys()
            logger.info("✅ 工具已退出")


def main():
    """主函数"""
    scanner = EquipmentScanner()
    
    # 保存配置（如果不存在）
    if not Path(CONFIG_FILE).exists():
        scanner.save_config()
        print(f"\n✅ 配置文件已生成：{CONFIG_FILE}")
    
    # 启动工具
    scanner.start()


if __name__ == "__main__":
    main()
