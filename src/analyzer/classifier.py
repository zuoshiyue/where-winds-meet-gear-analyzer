"""
职业分类模块
根据装备属性推荐适合的职业
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from ..database.models import ClassConfig, Equipment


@dataclass
class ClassMatch:
    """职业匹配结果"""

    class_name: str
    match_score: float  # 匹配度 (0-100)
    matched_stats: List[str]  # 匹配的属性
    recommended: bool  # 是否推荐


class ClassClassifier:
    """职业分类器"""

    def __init__(self, class_configs: List[ClassConfig]):
        """
        初始化分类器

        Args:
            class_configs: 职业配置列表
        """
        self.configs = {config.class_name: config for config in class_configs}
        self.default_class = "通用"

    def classify(
        self, equipment: Equipment, top_n: int = 3
    ) -> List[ClassMatch]:
        """
        根据装备属性分类适合的职业

        Args:
            equipment: 装备对象
            top_n: 返回前 N 个匹配职业

        Returns:
            职业匹配结果列表
        """
        if not equipment.stats:
            # 没有属性信息，返回默认
            return [
                ClassMatch(
                    class_name=self.default_class,
                    match_score=50.0,
                    matched_stats=[],
                    recommended=True,
                )
            ]

        matches = []
        for class_name, config in self.configs.items():
            match_score, matched_stats = self._calculate_match(
                equipment, config
            )
            matches.append(
                ClassMatch(
                    class_name=class_name,
                    match_score=match_score,
                    matched_stats=matched_stats,
                    recommended=False,
                )
            )

        # 按匹配度排序
        matches.sort(key=lambda m: m.match_score, reverse=True)

        # 标记推荐 (前 top_n 且分数>=60)
        for i, match in enumerate(matches[:top_n]):
            if match.match_score >= 60:
                match.recommended = True

        return matches[:top_n]

    def _calculate_match(
        self, equipment: Equipment, config: ClassConfig
    ) -> Tuple[float, List[str]]:
        """
        计算装备与职业的匹配度

        Args:
            equipment: 装备对象
            config: 职业配置

        Returns:
            (匹配度分数，匹配的属性列表)
        """
        stat_weights = config.stat_weights or {}
        if not stat_weights:
            return 50.0, []  # 无权重配置，返回默认分数

        # 检查套装匹配
        set_bonus = 0
        if config.preferred_sets and equipment.set_name:
            if equipment.set_name in config.preferred_sets:
                set_bonus = 20  # 套装匹配加 20 分

        # 计算属性匹配
        total_weight = 0
        matched_weight = 0
        matched_stats = []

        for stat in equipment.stats:
            stat_name = stat.get("name", "")
            if stat_name in stat_weights:
                weight = stat_weights[stat_name]
                total_weight += weight
                matched_weight += weight
                matched_stats.append(stat_name)
            else:
                total_weight += 0.5  # 未配置权重的属性给基础分

        # 计算匹配度
        if total_weight == 0:
            attr_score = 50.0
        else:
            attr_score = (matched_weight / total_weight) * 80

        # 最终分数 = 属性分 + 套装 bonus
        final_score = min(100, attr_score + set_bonus)

        return final_score, matched_stats

    def get_best_class(self, equipment: Equipment) -> Optional[str]:
        """
        获取最适合的职业

        Args:
            equipment: 装备对象

        Returns:
            职业名称
        """
        matches = self.classify(equipment, top_n=1)
        return matches[0].class_name if matches else self.default_class

    def get_recommended_sets(self, class_name: str) -> List[str]:
        """
        获取职业推荐的套装列表

        Args:
            class_name: 职业名称

        Returns:
            推荐套装列表
        """
        config = self.configs.get(class_name)
        if config:
            return config.preferred_sets or []
        return []

    def add_class_config(self, config: ClassConfig):
        """添加职业配置"""
        self.configs[config.class_name] = config

    def remove_class_config(self, class_name: str) -> bool:
        """移除职业配置"""
        if class_name in self.configs:
            del self.configs[class_name]
            return True
        return False

    @classmethod
    def from_configs(cls, configs: List[ClassConfig]) -> "ClassClassifier":
        """从配置列表创建分类器"""
        return cls(configs)
