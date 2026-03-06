"""
装备数据解析模块
从 OCR 结果中解析装备信息 (名称、属性、品质等)
"""

import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from .recognizer import OCRResult


@dataclass
class EquipmentData:
    """装备数据"""

    name: str = ""  # 装备名称
    type: str = ""  # 装备类型 (武器/防具/饰品)
    quality: int = 1  # 品质 (1-5)
    level: int = 0  # 强化等级
    set_name: str = ""  # 套装名称
    stats: List[Dict[str, Any]] = field(default_factory=list)  # 属性列表
    raw_text: List[str] = field(default_factory=list)  # 原始识别文本
    screenshot_path: str = ""  # 截图路径
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class EquipmentParser:
    """装备数据解析器"""

    # 品质颜色映射 (根据游戏实际颜色调整)
    QUALITY_COLORS = {
        "白": 1,
        "绿": 2,
        "蓝": 3,
        "紫": 4,
        "金": 5,
        "橙色": 5,
    }

    # 装备类型关键词
    EQUIPMENT_TYPES = {
        "武器": ["剑", "刀", "枪", "弓", "扇", "琴", "笔", "刃"],
        "防具": ["头盔", "铠甲", "护腕", "腰带", "靴子", "衣", "甲"],
        "饰品": ["项链", "戒指", "玉佩", "香囊", "护符"],
    }

    # 属性关键词
    STAT_KEYWORDS = {
        "attack": ["攻击", "武力"],
        "defense": ["防御", "护甲"],
        "health": ["生命", "气血"],
        "crit": ["暴击", "会心"],
        "crit_damage": ["爆伤", "暴击伤害", "会心伤害"],
        "element_damage": ["元素伤害", "火攻", "冰攻", "雷攻", "毒攻"],
        "speed": ["速度", "身法"],
    }

    def __init__(self):
        """初始化解析器"""
        # 编译正则表达式
        self.level_pattern = re.compile(r"[+｜](\d{1,2})")
        self.stat_pattern = re.compile(r"([+｜\-]?[\d.]+)([%‰]?)")
        self.quality_pattern = re.compile(r"([白绿蓝紫金橙]).*?(?:品质|色)")

    def parse(self, ocr_results: List[OCRResult]) -> EquipmentData:
        """
        从 OCR 结果解析装备数据

        Args:
            ocr_results: OCR 识别结果列表

        Returns:
            装备数据对象
        """
        # 提取所有文本
        texts = [r.text for r in ocr_results]
        raw_text = texts.copy()

        equipment = EquipmentData(raw_text=raw_text)

        # 解析装备名称 (通常是第一行)
        equipment.name = self._parse_name(texts)

        # 解析品质
        equipment.quality = self._parse_quality(texts)

        # 解析类型
        equipment.type = self._parse_type(equipment.name)

        # 解析强化等级
        equipment.level = self._parse_level(texts)

        # 解析套装名称
        equipment.set_name = self._parse_set_name(texts)

        # 解析属性
        equipment.stats = self._parse_stats(texts)

        return equipment

    def _parse_name(self, texts: List[str]) -> str:
        """解析装备名称"""
        if not texts:
            return ""

        # 通常名称在第一行或第二行
        for i, text in enumerate(texts[:3]):
            # 跳过纯数字或符号行
            if re.match(r"^[\+｜\d%‰.]+$", text):
                continue
            # 跳过品质行
            if "品质" in text or "色" in text:
                continue
            # 清理文本
            name = text.strip()
            if len(name) >= 2:
                return name

        return texts[0].strip() if texts else ""

    def _parse_quality(self, texts: List[str]) -> int:
        """解析品质"""
        full_text = "".join(texts)

        # 查找品质关键词
        for color, quality in self.QUALITY_COLORS.items():
            if color in full_text:
                return quality

        return 1  # 默认白色

    def _parse_type(self, name: str) -> str:
        """解析装备类型"""
        for eq_type, keywords in self.EQUIPMENT_TYPES.items():
            for keyword in keywords:
                if keyword in name:
                    return eq_type
        return "未知"

    def _parse_level(self, texts: List[str]) -> int:
        """解析强化等级"""
        full_text = "".join(texts)

        # 查找 +X 格式
        match = self.level_pattern.search(full_text)
        if match:
            return int(match.group(1))

        return 0

    def _parse_set_name(self, texts: List[str]) -> str:
        """解析套装名称"""
        for text in texts:
            if "套装" in text or "效果" in text:
                # 提取套装名称 (套装名称通常在"套装效果"之前)
                idx = text.find("套装")
                if idx > 0:
                    return text[:idx].strip()
                idx = text.find("效果")
                if idx > 0:
                    return text[:idx].strip()
        return ""

    def _parse_stats(self, texts: List[str]) -> List[Dict[str, Any]]:
        """解析属性列表"""
        stats = []

        for text in texts:
            # 跳过名称、品质等行
            if any(
                skip in text
                for skip in ["品质", "套装", "效果", "等级", "类型"]
            ):
                continue

            # 尝试匹配属性格式 (属性名 + 数值)
            stat = self._parse_single_stat(text)
            if stat:
                stats.append(stat)

        return stats

    def _parse_single_stat(self, text: str) -> Optional[Dict[str, Any]]:
        """解析单个属性"""
        # 查找属性名和数值
        for stat_name, keywords in self.STAT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 提取数值
                    match = self.stat_pattern.search(text)
                    if match:
                        value_str = match.group(1)
                        unit = match.group(2)

                        try:
                            value = float(value_str)
                            return {
                                "name": stat_name,
                                "value": value,
                                "unit": unit,
                                "display": f"{keyword} {value}{unit}",
                            }
                        except ValueError:
                            pass

        return None

    def parse_from_text(self, text: str) -> EquipmentData:
        """
        从纯文本解析装备数据

        Args:
            text: 装备描述文本

        Returns:
            装备数据对象
        """
        lines = text.strip().split("\n")
        # 模拟 OCR 结果
        ocr_results = [
            OCRResult(text=line, confidence=1.0, bbox=[[0, i * 20, 200, i * 20]])
            for i, line in enumerate(lines)
        ]
        return self.parse(ocr_results)

    def validate(self, equipment: EquipmentData) -> List[str]:
        """
        验证装备数据完整性

        Args:
            equipment: 装备数据

        Returns:
            警告信息列表
        """
        warnings = []

        if not equipment.name:
            warnings.append("缺少装备名称")

        if equipment.quality < 1 or equipment.quality > 5:
            warnings.append(f"品质值异常：{equipment.quality}")

        if not equipment.stats:
            warnings.append("未识别到属性信息")

        return warnings
