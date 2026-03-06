#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
燕云十六声 - 装备自动截图工具
燕云装备助手配套工具 - 自动捕获游戏内装备列表

功能:
- 热键触发截图 (默认 F9)
- 定时自动截图 (可选)
- 自动识别游戏窗口
- 截图自动保存 + 智能命名
- 可选：自动上传到网站

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

# 第三方库
try:
    import pyautogui
    from PIL import Image
    import pygetwindow as gw
    import keyboard
except ImportError as e:
    print(f"❌ 缺少依赖库：{e}")
    print("请运行：pip install -r requirements.txt")
    sys.exit(1)

# 配置
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "game_window_title": "燕云十六声",
    "capture_hotkey": "f9",
    "output_dir": "captures",
    "auto_upload": False,
    "upload_url": "",
    "timer_mode": False,
    "timer_interval": 30,
    "image_format": "png",
    "image_quality": 95,
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_capture.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutoCapture:
    """自动截图工具类"""
    
    def __init__(self, config=None):
        """初始化工具"""
        self.config = config or self.load_config()
        self.output_dir = Path(self.config["output_dir"])
        self.output_dir.mkdir(exist_ok=True)
        self.is_running = False
        self.game_window = None
        
        # 配置 pyautogui
        pyautogui.FAILSAFE = True  # 鼠标移到屏幕角落可停止
        pyautogui.PAUSE = 0.5
        
        logger.info("✅ 自动截图工具初始化完成")
        logger.info(f"📁 截图保存目录：{self.output_dir.absolute()}")
        logger.info(f"⌨️ 触发热键：{self.config['capture_hotkey']}")
    
    def load_config(self):
        """加载配置文件"""
        if Path(CONFIG_FILE).exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
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
                logger.info(f"📐 窗口位置：({self.game_window.left}, {self.game_window.top})")
                logger.info(f"📏 窗口大小：{self.game_window.width}x{self.game_window.height}")
                return True
            else:
                logger.warning(f"⚠️ 未找到游戏窗口，请确保游戏已启动")
                return False
        except Exception as e:
            logger.error(f"❌ 查找窗口失败：{e}")
            return False
    
    def capture_screen(self, region=None):
        """截图"""
        try:
            if region:
                # 截取指定区域
                screenshot = pyautogui.screenshot(region=region)
            else:
                # 截取全屏
                screenshot = pyautogui.screenshot()
            
            return screenshot
        except Exception as e:
            logger.error(f"❌ 截图失败：{e}")
            return None
    
    def capture_game_window(self):
        """截取游戏窗口"""
        if not self.game_window:
            if not self.find_game_window():
                return None
        
        try:
            # 激活窗口
            self.game_window.activate()
            time.sleep(0.5)
            
            # 获取窗口位置和大小
            region = (
                self.game_window.left,
                self.game_window.top,
                self.game_window.width,
                self.game_window.height
            )
            
            # 截图
            screenshot = self.capture_screen(region=region)
            return screenshot
        except Exception as e:
            logger.error(f"❌ 截取游戏窗口失败：{e}")
            return None
    
    def save_screenshot(self, screenshot, filename=None):
        """保存截图"""
        if not screenshot:
            return None
        
        try:
            # 生成文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"equip_{timestamp}.{self.config['image_format']}"
            
            # 保存路径
            filepath = self.output_dir / filename
            
            # 保存截图
            if self.config["image_format"].upper() == "PNG":
                screenshot.save(filepath, "PNG", optimize=True)
            else:
                screenshot.save(filepath, quality=self.config["image_quality"])
            
            logger.info(f"✅ 截图已保存：{filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ 保存截图失败：{e}")
            return None
    
    def upload_screenshot(self, filepath):
        """上传截图到网站（可选功能）"""
        if not self.config["auto_upload"]:
            return False
        
        if not self.config["upload_url"]:
            logger.warning("⚠️ 未配置上传 URL")
            return False
        
        try:
            import requests
            
            with open(filepath, 'rb') as f:
                files = {'file': (filepath.name, f)}
                response = requests.post(self.config["upload_url"], files=files)
            
            if response.status_code == 200:
                logger.info(f"✅ 上传成功：{response.json()}")
                return True
            else:
                logger.error(f"❌ 上传失败：{response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ 上传异常：{e}")
            return False
    
    def on_capture_hotkey(self):
        """热键触发截图回调"""
        logger.info("⌨️ 检测到截图热键")
        
        # 截图
        screenshot = self.capture_game_window()
        if screenshot:
            filepath = self.save_screenshot(screenshot)
            if filepath:
                # 可选：上传
                if self.config["auto_upload"]:
                    self.upload_screenshot(filepath)
                
                # 显示通知
                print(f"\n✅ 截图成功：{filepath.name}")
                print(f"   路径：{filepath.absolute()}")
                print("-" * 50)
    
    def start_timer_mode(self):
        """启动定时截图模式"""
        if not self.config["timer_mode"]:
            return
        
        interval = self.config["timer_interval"]
        logger.info(f"⏱️ 定时截图模式已启动，间隔：{interval}秒")
        
        while self.is_running:
            time.sleep(interval)
            self.on_capture_hotkey()
    
    def start(self):
        """启动工具"""
        self.is_running = True
        
        print("\n" + "=" * 50)
        print("🎮 燕云十六声 - 装备自动截图工具")
        print("=" * 50)
        print(f"📁 截图目录：{self.output_dir.absolute()}")
        print(f"⌨️ 热键：{self.config['capture_hotkey']}")
        print(f"⏱️ 定时模式：{'开启' if self.config['timer_mode'] else '关闭'}")
        if self.config["timer_mode"]:
            print(f"   间隔：{self.config['timer_interval']}秒")
        print(f"🌐 自动上传：{'开启' if self.config['auto_upload'] else '关闭'}")
        print("=" * 50)
        print("\n💡 使用说明:")
        print("  - 按 F9 截图游戏窗口")
        print("  - 鼠标移到屏幕左上角可紧急停止")
        print("  - 按 Ctrl+C 退出程序")
        print("-" * 50)
        
        # 查找游戏窗口
        self.find_game_window()
        
        # 注册热键
        hotkey = self.config["capture_hotkey"]
        keyboard.add_hotkey(hotkey, self.on_capture_hotkey)
        logger.info(f"✅ 热键已注册：{hotkey}")
        
        # 启动定时模式（可选）
        if self.config["timer_mode"]:
            import threading
            timer_thread = threading.Thread(target=self.start_timer_mode, daemon=True)
            timer_thread.start()
        
        # 主循环
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            logger.info("👋 正在退出...")
        finally:
            self.is_running = False
            keyboard.remove_all_hotkeys()
            logger.info("✅ 工具已退出")


def main():
    """主函数"""
    # 创建工具实例
    capturer = AutoCapture()
    
    # 保存配置（如果不存在）
    if not Path(CONFIG_FILE).exists():
        capturer.save_config()
        print(f"\n✅ 配置文件已生成：{CONFIG_FILE}")
        print("💡 可以修改配置文件自定义设置")
    
    # 启动工具
    capturer.start()


if __name__ == "__main__":
    main()
