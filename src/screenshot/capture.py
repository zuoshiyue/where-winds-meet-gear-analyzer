"""
截图捕获模块
提供游戏窗口截图功能，支持全屏截图和指定区域截图
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import mss
import mss.tools
from PIL import Image
import numpy as np


class ScreenshotCapture:
    """游戏截图捕获器"""

    def __init__(
        self,
        save_dir: str = "data/screenshots",
        format: str = "png",
        compress_level: int = 6,
        window_title: Optional[str] = None,
    ):
        """
        初始化截图捕获器

        Args:
            save_dir: 截图保存目录
            format: 截图格式 (png, jpg)
            compress_level: PNG 压缩级别 (1-9)
            window_title: 游戏窗口标题
        """
        self.save_dir = Path(save_dir)
        self.format = format.lower()
        self.compress_level = compress_level
        self.window_title = window_title

        # 确保保存目录存在
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # MSS 截图实例
        self.sct = mss.mss()

    def find_game_window(self) -> Optional[dict]:
        """
        查找游戏窗口

        Returns:
            窗口信息字典，包含 'left', 'top', 'width', 'height'，找不到返回 None
        """
        if not self.window_title:
            return None

        # 遍历所有显示器查找匹配窗口
        for monitor in self.sct.monitors[1:]:  # 跳过主显示器 (index 0)
            # 注意：mss 不直接支持窗口查找，需要结合其他库
            # 这里简化处理，返回第一个显示器
            # 实际项目中可以使用 pygetwindow 来查找特定窗口
            return monitor

        return None

    def capture(
        self,
        region: Optional[Tuple[int, int, int, int]] = None,
        filename: Optional[str] = None,
        save: bool = True,
    ) -> Optional[np.ndarray]:
        """
        执行截图

        Args:
            region: 截图区域 (left, top, width, height)，None 表示全屏
            filename: 保存文件名，None 则自动生成
            save: 是否保存到文件

        Returns:
            截图的 numpy 数组 (RGB 格式)，失败返回 None
        """
        try:
            # 确定截图区域
            if region:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3],
                }
            else:
                # 使用第一个显示器
                monitor = self.sct.monitors[1] if len(self.sct.monitors) > 1 else self.sct.monitors[0]

            # 执行截图
            screenshot = self.sct.grab(monitor)

            # 转换为 PIL Image (BGRA 格式)
            img = Image.frombytes("RGBA", screenshot.size, screenshot.bgra, "raw", "BGRA")

            # 转换为 RGB 格式 (numpy 数组)
            img_rgb = img.convert("RGB")
            result = np.array(img_rgb)

            # 保存文件
            if save:
                save_path = self._generate_filename(filename)
                self._save_image(img_rgb, save_path)
                print(f"截图已保存：{save_path}")

            return result

        except Exception as e:
            print(f"截图失败：{e}")
            return None

    def _generate_filename(self, filename: Optional[str] = None) -> Path:
        """生成文件名"""
        if filename:
            return self.save_dir / filename

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"screenshot_{timestamp}.{self.format}"
        return self.save_dir / filename

    def _save_image(self, img: Image.Image, path: Path) -> None:
        """保存图片"""
        if self.format == "png":
            img.save(path, "PNG", compress_level=self.compress_level)
        elif self.format == "jpg":
            img.convert("RGB").save(path, "JPEG", quality=95)
        else:
            img.save(path)

    def capture_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        filename: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        截取指定区域

        Args:
            left: 区域左边距
            top: 区域上边距
            width: 区域宽度
            height: 区域高度
            filename: 保存文件名

        Returns:
            截图的 numpy 数组
        """
        region = (left, top, width, height)
        return self.capture(region=region, filename=filename)

    def capture_full_screen(self, filename: Optional[str] = None) -> Optional[np.ndarray]:
        """
        截取全屏

        Args:
            filename: 保存文件名

        Returns:
            截图的 numpy 数组
        """
        return self.capture(region=None, filename=filename)

    @staticmethod
    def list_monitors() -> list:
        """列出所有可用显示器"""
        with mss.mss() as sct:
            monitors = []
            for i, monitor in enumerate(sct.monitors[1:], 1):
                monitors.append(
                    {
                        "index": i,
                        "left": monitor["left"],
                        "top": monitor["top"],
                        "width": monitor["width"],
                        "height": monitor["height"],
                    }
                )
            return monitors


# 快捷键截图支持
class HotkeyCapture:
    """快捷键截图支持"""

    def __init__(self, capture: ScreenshotCapture):
        """
        初始化快捷键截图

        Args:
            capture: ScreenshotCapture 实例
        """
        self.capture = capture
        self.hotkey_callback = None
        self.listening = False

    def register_hotkey(self, hotkey: str = "f12", callback: Optional[callable] = None):
        """
        注册截图快捷键

        Args:
            hotkey: 快捷键
            callback: 回调函数，接收截图路径
        """
        self.hotkey_callback = callback or self._default_callback
        print(f"注册快捷键：{hotkey} (需要额外实现监听)")
        # 注意：实际实现需要使用 pynput 或 keyboard 库
        # 这里提供接口，具体实现在 UI 模块中完成

    def _default_callback(self, filepath: str):
        """默认回调"""
        print(f"截图已保存：{filepath}")

    def start_listening(self):
        """开始监听快捷键"""
        self.listening = True
        # 实际实现需要启动监听线程

    def stop_listening(self):
        """停止监听快捷键"""
        self.listening = False
