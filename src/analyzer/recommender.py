"""
装备推荐模块
根据评分结果生成培养建议和替换推荐
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

from ..database.models import Equipment, ClassConfig
from .scorer import EquipmentScorer, ScoreResult


@dataclass
class Recommendation:
    """培养建议"""

    equipment_id: int
    equipment_name: str
    action: str  # 建议操作：keep/upgrade/replace/material/sell
    priority: str  # 优先级：high/medium/low
    reason: str  # 原因
    details: List[str] = field(default_factory=list)  # 详细说明


@dataclass
class ReplacementSuggestion:
    """替换建议"""

    current_equipment: Equipment
    replacement: Equipment
    score_improvement: float
    reasons: List[str]


class EquipmentRecommender:
    """装备推荐器"""

    # 操作类型
    ACTION_KEEP = "keep"  # 保留使用
    ACTION_UPGRADE = "upgrade"  # 建议强化
    ACTION_REPLACE = "replace"  # 建议替换
    ACTION_MATERIAL = "material"  # 作为强化材料
    ACTION_SELL = "sell"  # 出售/分解

    # 优先级
    PRIORITY_HIGH = "high"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_LOW = "low"

    def __init__(self, scorer: EquipmentScorer):
        """
        初始化推荐器

        Args:
            scorer: 评分器实例
        """
        self.scorer = scorer

    def recommend(
        self,
        equipment: Equipment,
        score_result: ScoreResult,
        class_config: Optional[ClassConfig] = None,
    ) -> Recommendation:
        """
        生成培养建议

        Args:
            equipment: 装备对象
            score_result: 评分结果
            class_config: 职业配置

        Returns:
            培养建议
        """
        action = self._determine_action(equipment, score_result, class_config)
        priority = self._determine_priority(score_result, equipment)
        reason = self._generate_reason(equipment, score_result, action)
        details = self._generate_details(equipment, score_result, class_config)

        return Recommendation(
            equipment_id=equipment.id,
            equipment_name=equipment.name,
            action=action,
            priority=priority,
            reason=reason,
            details=details,
        )

    def _determine_action(
        self,
        equipment: Equipment,
        score_result: ScoreResult,
        class_config: Optional[ClassConfig],
    ) -> str:
        """确定建议操作"""
        score = score_result.total_score

        # 高分装备：保留
        if score >= 180:
            return self.ACTION_KEEP

        # 中等分数 + 高品质：建议强化
        if score >= 120 and equipment.quality >= 4 and equipment.level < 15:
            return self.ACTION_UPGRADE

        # 低分高质：可能是属性不匹配，作为材料
        if score < 100 and equipment.quality >= 4:
            return self.ACTION_MATERIAL

        # 低分低质：出售/分解
        if score < 80 and equipment.quality <= 2:
            return self.ACTION_SELL

        # 中等分数：根据套装决定
        if class_config and equipment.set_name:
            if equipment.set_name in (class_config.preferred_sets or []):
                return self.ACTION_KEEP

        # 默认保留
        return self.ACTION_KEEP

    def _determine_priority(
        self, score_result: ScoreResult, equipment: Equipment
    ) -> str:
        """确定优先级"""
        score = score_result.total_score

        if score >= 150 or equipment.quality >= 4:
            return self.PRIORITY_HIGH
        elif score >= 100 or equipment.quality >= 3:
            return self.PRIORITY_MEDIUM
        else:
            return self.PRIORITY_LOW

    def _generate_reason(
        self,
        equipment: Equipment,
        score_result: ScoreResult,
        action: str,
    ) -> str:
        """生成原因说明"""
        reasons = []

        if action == self.ACTION_KEEP:
            if score_result.total_score >= 180:
                reasons.append("评分优秀")
            if equipment.quality >= 4:
                reasons.append("品质较高")
            if score_result.set_bonus > 0:
                reasons.append("套装契合")

        elif action == self.ACTION_UPGRADE:
            reasons.append("有培养潜力")
            if equipment.level < 5:
                reasons.append("强化空间大")

        elif action == self.ACTION_MATERIAL:
            reasons.append("属性不匹配当前职业")
            reasons.append("但品质较好")

        elif action == self.ACTION_SELL:
            reasons.append("评分较低")
            reasons.append("品质一般")

        return "，".join(reasons)

    def _generate_details(
        self,
        equipment: Equipment,
        score_result: ScoreResult,
        class_config: Optional[ClassConfig],
    ) -> List[str]:
        """生成详细说明"""
        details = []

        # 评分分析
        details.append(f"总评分：{score_result.total_score:.1f}")
        details.append(
            f"  - 品质分：{score_result.quality_score:.1f}"
        )
        details.append(
            f"  - 属性分：{score_result.stats_score:.1f}"
        )
        details.append(
            f"  - 强化分：{score_result.level_score:.1f}"
        )

        # 套装分析
        if equipment.set_name:
            details.append(f"套装：{equipment.set_name}")
            if class_config:
                if equipment.set_name in (class_config.preferred_sets or []):
                    details.append("  ✓ 推荐套装")
                else:
                    details.append("  - 非推荐套装")

        # 属性分析
        if equipment.stats:
            best_stat = max(
                equipment.stats,
                key=lambda s: self.scorer.stat_weights.get(s.get("name", ""), 0),
            )
            details.append(f"核心属性：{best_stat.get('display', '')}")

        return details

    def find_replacements(
        self,
        current_equipment: Equipment,
        candidate_list: List[Equipment],
        equipment_type: Optional[str] = None,
        class_config: Optional[ClassConfig] = None,
    ) -> List[ReplacementSuggestion]:
        """
        查找可替换的装备

        Args:
            current_equipment: 当前装备
            candidate_list: 候选装备列表
            equipment_type: 装备类型 (可选，用于筛选同类型)
            class_config: 职业配置

        Returns:
            替换建议列表
        """
        suggestions = []

        # 计算当前装备评分
        current_score = self.scorer.score(
            current_equipment,
            class_config.class_name if class_config else "通用",
            class_config,
        ).total_score

        # 筛选同类型装备
        if equipment_type:
            candidates = [
                eq for eq in candidate_list
                if eq.type == equipment_type and eq.id != current_equipment.id
            ]
        else:
            candidates = [
                eq for eq in candidate_list
                if eq.id != current_equipment.id
            ]

        # 查找更好的装备
        for candidate in candidates:
            candidate_score = self.scorer.score(
                candidate,
                class_config.class_name if class_config else "通用",
                class_config,
            ).total_score

            if candidate_score > current_score:
                improvement = candidate_score - current_score
                reasons = self._compare_equipment(
                    current_equipment, candidate, class_config
                )
                suggestions.append(
                    ReplacementSuggestion(
                        current_equipment=current_equipment,
                        replacement=candidate,
                        score_improvement=improvement,
                        reasons=reasons,
                    )
                )

        # 按提升分数排序
        suggestions.sort(key=lambda s: s.score_improvement, reverse=True)

        return suggestions[:5]  # 返回前 5 个

    def _compare_equipment(
        self,
        eq1: Equipment,
        eq2: Equipment,
        class_config: Optional[ClassConfig],
    ) -> List[str]:
        """比较两件装备，返回差异原因"""
        reasons = []

        # 品质对比
        if eq2.quality > eq1.quality:
            reasons.append(f"品质提升 ({eq1.quality} -> {eq2.quality})")

        # 强化等级对比
        if eq2.level > eq1.level:
            reasons.append(f"强化等级更高 (+{eq2.level - eq1.level})")

        # 套装对比
        if class_config and class_config.preferred_sets:
            if eq2.set_name in class_config.preferred_sets:
                if eq1.set_name not in class_config.preferred_sets:
                    reasons.append("套装更契合")

        # 属性对比
        if eq2.stats and not eq1.stats:
            reasons.append("属性更丰富")

        return reasons

    def get_gear_priority(
        self,
        equipment_list: List[Equipment],
        class_config: Optional[ClassConfig] = None,
    ) -> List[Tuple[Equipment, Recommendation]]:
        """
        获取装备培养优先级排序

        Args:
            equipment_list: 装备列表
            class_config: 职业配置

        Returns:
            (装备，建议) 列表，按优先级排序
        """
        results = []

        for equipment in equipment_list:
            score_result = self.scorer.score(
                equipment,
                class_config.class_name if class_config else "通用",
                class_config,
            )
            recommendation = self.recommend(equipment, score_result, class_config)
            results.append((equipment, recommendation))

        # 按优先级排序
        priority_order = {
            self.PRIORITY_HIGH: 0,
            self.PRIORITY_MEDIUM: 1,
            self.PRIORITY_LOW: 2,
        }
        results.sort(
            key=lambda x: (
                priority_order.get(x[1].priority, 3),
                -x[0].id,  # 同优先级按 ID 降序
            )
        )

        return results
