"""
图像预处理模块
对截图进行去噪、增强、二值化等预处理操作，提升 OCR 识别率
"""

from typing import Optional, Tuple
import numpy as np
import cv2


class ImagePreprocessor:
    """图像预处理器"""

    def __init__(
        self,
        denoise: bool = True,
        enhance_contrast: bool = True,
        binarize: bool = False,
        blur_kernel: int = 3,
    ):
        """
        初始化预处理器

        Args:
            denoise: 是否去噪
            enhance_contrast: 是否增强对比度
            binarize: 是否二值化
            blur_kernel: 高斯模糊核大小 (奇数)
        """
        self.denoise = denoise
        self.enhance_contrast = enhance_contrast
        self.binarize = binarize
        self.blur_kernel = blur_kernel

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        执行图像预处理

        Args:
            image: 输入图像 (RGB 或灰度)

        Returns:
            预处理后的图像
        """
        result = image.copy()

        # 转换为灰度图
        if len(result.shape) == 3:
            gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        else:
            gray = result

        # 高斯模糊去噪
        if self.denoise:
            gray = cv2.GaussianBlur(gray, (self.blur_kernel, self.blur_kernel), 0)

        # 对比度增强
        if self.enhance_contrast:
            gray = self._enhance_contrast(gray)

        # 二值化
        if self.binarize:
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return gray

    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        增强图像对比度 (CLAHE)

        Args:
            image: 灰度图像

        Returns:
            对比度增强后的图像
        """
        # 创建 CLAHE 对象
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)

    def crop_roi(
        self,
        image: np.ndarray,
        margins: Optional[Tuple[int, int, int, int]] = None,
        roi: Optional[Tuple[int, int, int, int]] = None,
    ) -> np.ndarray:
        """
        裁剪感兴趣区域

        Args:
            image: 输入图像
            margins: 边距裁剪 (top, bottom, left, right)
            roi: ROI 区域 (x, y, w, h)

        Returns:
            裁剪后的图像
        """
        if roi:
            x, y, w, h = roi
            return image[y : y + h, x : x + w]

        if margins:
            top, bottom, left, right = margins
            return image[top:-bottom, left:-right]

        return image

    @staticmethod
    def resize_by_scale(
        image: np.ndarray, scale: float, interpolation: int = cv2.INTER_CUBIC
    ) -> np.ndarray:
        """
        按比例缩放图像

        Args:
            image: 输入图像
            scale: 缩放比例
            interpolation: 插值方法

        Returns:
            缩放后的图像
        """
        height, width = image.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        return cv2.resize(image, (new_width, new_height), interpolation=interpolation)

    @staticmethod
    def deskew(image: np.ndarray) -> np.ndarray:
        """
        校正图像倾斜

        Args:
            image: 灰度图像

        Returns:
            校正后的图像
        """
        # 计算图像的矩
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        # 调整角度
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # 旋转校正
        if abs(angle) > 0.5:  # 只有明显倾斜才校正
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(
                image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
            )

        return image
