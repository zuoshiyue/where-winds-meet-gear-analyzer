"""OCR 模块 - 光学字符识别"""

from .recognizer import OCRRecognizer
from .parser import EquipmentParser
from .preprocessor import ImagePreprocessor

__all__ = ["OCRRecognizer", "EquipmentParser", "ImagePreprocessor"]
