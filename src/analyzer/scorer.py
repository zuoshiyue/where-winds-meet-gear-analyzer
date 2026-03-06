"""
装备评分模块
根据职业配置计算装备评分
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..database.models import Equipment, ClassConfig, ScoreRecord


@dataclass
class ScoreResult:
    """评分结果"""

    total_score: float  # 总分
    sub_scores: Dict[str, float] = field(default_factory=dict)  # 分项评分
    quality_score: float = 0.0  # 品质分
    stats_score: float = 0.0  # 属性分
    level_score: float = 0.0  # 强化分
    set_bonus: float = 0.0  # 套装加成
    recommendation: str = ""  # 培养建议
    class_name: str = ""  # 评分职业
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_score_record(self, equipment_id: int) -> ScoreRecord:
        """转换为数据库记录"""
        return ScoreRecord(
            equipment_id=equipment_id,
            class_name=self.class_name,
            total_score=self.total_score,
            sub_scores=self.sub_scores,
            recommendation=self.recommendation,
        )


class EquipmentScorer:
    """装备评分器"""

    # 品质基础分配置
    DEFAULT_QUALITY_SCORES = {
        1: 10,  # 白色
        2: 30,  # 绿色
        3: 60,  # 蓝色
        4: 100,  # 紫色
        5: 150,  # 金色
    }

    # 默认属性权重
    DEFAULT_STAT_WEIGHTS = {
        "attack": 1.0,
        "defense": 0.8,
        "health": 0.7,
        "crit": 1.5,
        "crit_damage": 1.5,
        "element_damage": 1.3,
        "speed": 1.0,
    }

    # 强化等级系数
    LEVEL_MULTIPLIER = 0.1

    def __init__(
        self,
        quality_scores: Optional[Dict[int, float]] = None,
        stat_weights: Optional[Dict[str, float]] = None,
        level_multiplier: float = 0.1,
    ):
        """
        初始化评分器

        Args:
            quality_scores: 品质分数配置
            stat_weights: 属性权重配置
            level_multiplier: 强化等级系数
        """
        self.quality_scores = quality_scores or self.DEFAULT_QUALITY_SCORES
        self.stat_weights = stat_weights or self.DEFAULT_STAT_WEIGHTS
        self.level_multiplier = level_multiplier

    def score(
        self,
        equipment: Equipment,
        class_name: str = "通用",
        class_config: Optional[ClassConfig] = None,
    ) -> ScoreResult:
        """
        计算装备评分

        Args:
            equipment: 装备对象
            class_name: 职业名称
            class_config: 职业配置 (可选，用于自定义权重)

        Returns:
            评分结果
        """
        result = ScoreResult(class_name=class_name)

        # 1. 品质分
        result.quality_score = self._calc_quality_score(equipment.quality)

        # 2. 属性分
        weights = self._get_stat_weights(class_config)
        result.stats_score = self._calc_stats_score(equipment.stats, weights)

        # 3. 强化分
        result.level_score = self._calc_level_score(equipment.level)

        # 4. 套装加成
        result.set_bonus = self._calc_set_bonus(equipment, class_config)

        # 5. 计算总分
        result.total_score = (
            result.quality_score
            + result.stats_score
            + result.level_score
            + result.set_bonus
        )

        # 6. 记录分项评分
        result.sub_scores = {
            "品质": result.quality_score,
            "属性": result.stats_score,
            "强化": result.level_score,
            "套装": result.set_bonus,
        }

        # 7. 生成培养建议
        result.recommendation = self._generate_recommendation(
            equipment, result, class_config
        )

        return result

    def _calc_quality_score(self, quality: int) -> float:
        """计算品质分"""
        return self.quality_scores.get(quality, 10)

    def _calc_stats_score(
        self, stats: List[Dict[str, Any]], weights: Dict[str, float]
    ) -> float:
        """计算属性分"""
        if not stats:
            return 0.0

        total_score = 0.0
        for stat in stats:
            stat_name = stat.get("name", "")
            value = stat.get("value", 0)
            weight = weights.get(stat_name, 0.5)

            # 分数 = 数值 * 权重
            total_score += value * weight

        return total_score

    def _calc_level_score(self, level: int) -> float:
        """计算强化分"""
        # 强化分 = 等级 * 等级系数 * (1 + 等级/10)
        # 高等级有额外加成
        base = level * self.level_multiplier * 10
        bonus = (level / 10) * self.level_multiplier * 5
        return base + bonus

    def _calc_set_bonus(
        self, equipment: Equipment, class_config: Optional[ClassConfig]
    ) -> float:
        """计算套装加成"""
        if not equipment.set_name:
            return 0.0

        # 检查是否是推荐套装
        if class_config and class_config.preferred_sets:
            if equipment.set_name in class_config.preferred_sets:
                return 20.0  # 推荐套装加 20 分

        return 5.0  # 非推荐套装加 5 分

    def _get_stat_weights(
        self, class_config: Optional[ClassConfig]
    ) -> Dict[str, float]:
        """获取属性权重"""
        if class_config and class_config.stat_weights:
            return class_config.stat_weights
        return self.stat_weights

    def _generate_recommendation(
        self,
        equipment: Equipment,
        result: ScoreResult,
        class_config: Optional[ClassConfig],
    ) -> str:
        """生成培养建议"""
        suggestions = []

        # 根据总分给建议
        if result.total_score >= 200:
            suggestions.append("极品装备，建议优先培养")
        elif result.total_score >= 150:
            suggestions.append("优秀装备，值得培养")
        elif result.total_score >= 100:
            suggestions.append("普通装备，过渡使用")
        else:
            suggestions.append("建议替换")

        # 根据品质给建议
        if equipment.quality >= 4:
            suggestions.append("高品质装备，建议保留")
        elif equipment.quality <= 2:
            suggestions.append("品质较低，可作为强化材料")

        # 根据强化等级给建议
        if equipment.level >= 10:
            suggestions.append("已高度强化，建议继续使用")
        elif equipment.level == 0 and equipment.quality >= 3:
            suggestions.append("未强化，建议投入资源")

        # 根据套装给建议
        if class_config and equipment.set_name:
            if equipment.set_name in (class_config.preferred_sets or []):
                suggestions.append("套装契合度高，推荐作为毕业装备")

        return "；".join(suggestions)

    def compare(
        self, equipment1: Equipment, equipment2: Equipment, class_name: str = "通用"
    ) -> Dict[str, Any]:
        """
        对比两件装备

        Args:
            equipment1: 装备 1
            equipment2: 装备 2
            class_name: 职业名称

        Returns:
            对比结果
        """
        score1 = self.score(equipment1, class_name)
        score2 = self.score(equipment2, class_name)

        diff = score1.total_score - score2.total_score

        return {
            "equipment1": {
                "name": equipment1.name,
                "score": score1.total_score,
                "sub_scores": score1.sub_scores,
            },
            "equipment2": {
                "name": equipment2.name,
                "score": score2.total_score,
                "sub_scores": score2.sub_scores,
            },
            "better": equipment1.name if diff > 0 else equipment2.name,
            "score_diff": abs(diff),
        }

    def bulk_score(
        self,
        equipment_list: List[Equipment],
        class_name: str = "通用",
        class_config: Optional[ClassConfig] = None,
    ) -> List[ScoreResult]:
        """
        批量评分

        Args:
            equipment_list: 装备列表
            class_name: 职业名称
            class_config: 职业配置

        Returns:
            评分结果列表
        """
        return [
            self.score(eq, class_name, class_config) for eq in equipment_list
        ]
