"""
OCR 识别模块
使用 PaddleOCR 进行装备信息的文字识别
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class OCRResult:
    """OCR 识别结果"""

    text: str
    confidence: float
    bbox: List[List[int]]  # 四个角点坐标 [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]


class OCRRecognizer:
    """OCR 识别器"""

    def __init__(
        self,
        lang: str = "ch",
        use_gpu: bool = False,
        confidence_threshold: float = 0.6,
    ):
        """
        初始化 OCR 识别器

        Args:
            lang: 识别语言 (ch: 简体中文，en: 英文)
            use_gpu: 是否使用 GPU
            confidence_threshold: 置信度阈值
        """
        self.lang = lang
        self.use_gpu = use_gpu
        self.confidence_threshold = confidence_threshold
        self._ocr_engine = None

    def _init_engine(self):
        """延迟初始化 OCR 引擎"""
        if self._ocr_engine is None:
            try:
                from paddleocr import PaddleOCR

                self._ocr_engine = PaddleOCR(
                    use_angle_cls=True,
                    lang=self.lang,
                    use_gpu=self.use_gpu,
                    show_log=False,
                )
            except ImportError:
                print("错误：请安装 paddleocr 库 (pip install paddleocr)")
                raise

    def recognize(self, image: np.ndarray) -> List[OCRResult]:
        """
        识别图像中的文字

        Args:
            image: 输入图像 (RGB 或灰度)

        Returns:
            OCR 结果列表
        """
        self._init_engine()

        # 执行 OCR 识别
        result = self._ocr_engine.ocr(image, cls=True)

        # 解析结果
        ocr_results = []
        if result and result[0]:
            for item in result[0]:
                bbox = item[0]
                text = item[1][0]
                confidence = item[1][1]

                if confidence >= self.confidence_threshold:
                    ocr_results.append(
                        OCRResult(text=text, confidence=confidence, bbox=bbox)
                    )

        return ocr_results

    def recognize_text(self, image: np.ndarray) -> str:
        """
        识别图像中的文字 (只返回文本)

        Args:
            image: 输入图像

        Returns:
            识别的文本内容
        """
        results = self.recognize(image)
        return " ".join([r.text for r in results])

    def recognize_region(
        self, image: np.ndarray, region: tuple
    ) -> List[OCRResult]:
        """
        识别指定区域的文字

        Args:
            image: 输入图像
            region: 区域坐标 (x, y, w, h)

        Returns:
            OCR 结果列表
        """
        x, y, w, h = region
        roi = image[y : y + h, x : x + w]
        return self.recognize(roi)

    @staticmethod
    def sort_results_by_position(
        results: List[OCRResult], top_to_bottom: bool = True
    ) -> List[OCRResult]:
        """
        按位置排序 OCR 结果

        Args:
            results: OCR 结果列表
            top_to_bottom: True 从上到下，False 从左到右

        Returns:
            排序后的结果列表
        """
        if not results:
            return []

        if top_to_bottom:
            # 按 Y 坐标排序
            return sorted(results, key=lambda r: r.bbox[0][1])
        else:
            # 按 X 坐标排序
            return sorted(results, key=lambda r: r.bbox[0][0])

    def batch_recognize(
        self, images: List[np.ndarray]
    ) -> List[List[OCRResult]]:
        """
        批量识别多张图像

        Args:
            images: 图像列表

        Returns:
            每张图的 OCR 结果列表
        """
        return [self.recognize(img) for img in images]
