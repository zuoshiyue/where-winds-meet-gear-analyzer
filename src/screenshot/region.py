"""
区域识别模块
识别游戏界面中的特定区域 (背包、装备详情等)
"""

from typing import Optional, Tuple, List, Dict
import numpy as np
import cv2


class RegionDetector:
    """游戏界面区域检测器"""

    def __init__(self):
        """初始化区域检测器"""
        # 预定义的游戏界面区域模板
        self.templates = {}

    def add_template(self, name: str, template_path: str, threshold: float = 0.8):
        """
        添加区域模板

        Args:
            name: 区域名称
            template_path: 模板图片路径
            threshold: 匹配阈值
        """
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise ValueError(f"无法加载模板图片：{template_path}")
        self.templates[name] = {"image": template, "threshold": threshold}

    def find_region(
        self, screenshot: np.ndarray, region_name: str
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        在截图中查找指定区域

        Args:
            screenshot: 截图 (RGB 格式)
            region_name: 区域名称

        Returns:
            区域坐标 (x, y, w, h)，未找到返回 None
        """
        if region_name not in self.templates:
            print(f"未知区域：{region_name}")
            return None

        template_info = self.templates[region_name]
        template = template_info["image"]
        threshold = template_info["threshold"]

        # 转换为灰度图
        if len(screenshot.shape) == 3:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        else:
            gray = screenshot

        # 模板匹配
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape
            return (max_loc[0], max_loc[1], w, h)

        return None

    def find_all_regions(
        self, screenshot: np.ndarray
    ) -> Dict[str, Optional[Tuple[int, int, int, int]]]:
        """
        查找所有已注册的区域

        Args:
            screenshot: 截图

        Returns:
            区域字典 {name: (x, y, w, h) or None}
        """
        results = {}
        for name in self.templates.keys():
            results[name] = self.find_region(screenshot, name)
        return results

    def find_backpack_region(
        self, screenshot: np.ndarray
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        查找背包界面区域

        Args:
            screenshot: 截图

        Returns:
            背包区域坐标
        """
        return self.find_region(screenshot, "backpack")

    def find_equipment_detail_region(
        self, screenshot: np.ndarray
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        查找装备详情区域

        Args:
            screenshot: 截图

        Returns:
            详情区域坐标
        """
        return self.find_region(screenshot, "equipment_detail")


class GridDetector:
    """背包格子检测器"""

    def __init__(
        self, grid_size: Tuple[int, int] = (5, 10), cell_size: Tuple[int, int] = (80, 80)
    ):
        """
        初始化格子检测器

        Args:
            grid_size: 背包格子行列数 (rows, cols)
            cell_size: 每个格子的大小 (width, height)
        """
        self.rows, self.cols = grid_size
        self.cell_width, self.cell_height = cell_size

    def detect_cells(
        self, region: Tuple[int, int, int, int], gap: int = 5
    ) -> List[Tuple[int, int, int, int]]:
        """
        检测所有格子坐标

        Args:
            region: 背包区域 (x, y, w, h)
            gap: 格子间距

        Returns:
            格子坐标列表 [(x, y, w, h), ...]
        """
        x0, y0, w, h = region
        cells = []

        for row in range(self.rows):
            for col in range(self.cols):
                cell_x = x0 + col * (self.cell_width + gap) + gap
                cell_y = y0 + row * (self.cell_height + gap) + gap
                cells.append((cell_x, cell_y, self.cell_width, self.cell_height))

        return cells

    def detect_empty_cells(
        self, screenshot: np.ndarray, cells: List[Tuple[int, int, int, int]]
    ) -> List[int]:
        """
        检测空格子索引

        Args:
            screenshot: 截图
            cells: 格子坐标列表

        Returns:
            空格子索引列表
        """
        empty_cells = []

        for i, (x, y, w, h) in enumerate(cells):
            cell_img = screenshot[y : y + h, x : x + w]

            # 简单的空检测：平均亮度
            if len(cell_img.shape) == 3:
                gray = cv2.cvtColor(cell_img, cv2.COLOR_RGB2GRAY)
            else:
                gray = cell_img

            # 如果大部分区域是暗色，认为是空格子
            avg_brightness = np.mean(gray)
            if avg_brightness < 50:  # 阈值可调
                empty_cells.append(i)

        return empty_cells
