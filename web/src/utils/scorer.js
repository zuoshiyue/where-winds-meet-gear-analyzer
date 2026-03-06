/**
 * 装备评分模块
 * 根据职业配置计算装备评分
 */

// 品质基础分
const QUALITY_SCORES = {
  1: 10,  // 白色
  2: 30,  // 绿色
  3: 60,  // 蓝色
  4: 100, // 紫色
  5: 150, // 金色
}

// 默认属性权重
const DEFAULT_STAT_WEIGHTS = {
  attack: 1.0,
  defense: 0.8,
  health: 0.7,
  crit: 1.5,
  crit_damage: 1.5,
  element_damage: 1.3,
  speed: 1.0,
}

// 职业配置 (根据燕云十六声实际职业)
const CLASS_CONFIGS = {
  '通用': {
    preferred_sets: [],
    stat_weights: DEFAULT_STAT_WEIGHTS,
    description: '通用配置，适合所有职业',
  },
  '剑客': {
    preferred_sets: ['剑心套装', '疾风套装', '暴击套装'],
    stat_weights: {
      attack: 1.5,      // 高优先级 - 主要输出属性
      defense: 1.0,     // 中等优先级 - 攻守兼备
      health: 0.8,      // 中等优先级 - 生存能力
      crit: 1.8,        // 高优先级 - 暴击输出
      crit_damage: 1.8, // 高优先级 - 爆伤加成
      element_damage: 1.3, // 中等优先级 - 元素伤害
      speed: 1.5,       // 高优先级 - 攻速移速
    },
    description: '近战输出，攻守兼备，高机动性',
  },
  '刀客': {
    preferred_sets: ['霸刀套装', '铁血套装', '强攻套装'],
    stat_weights: {
      attack: 1.8,      // 最高优先级 - 极致输出
      defense: 0.6,     // 低优先级 - 牺牲防御
      health: 0.6,      // 低优先级 - 牺牲生存
      crit: 1.6,        // 高优先级 - 暴击加成
      crit_damage: 1.9, // 最高优先级 - 爆伤最大化
      element_damage: 1.4, // 中等优先级
      speed: 1.2,       // 中等优先级
    },
    description: '近战高攻击，快速击倒敌人',
  },
  '枪客': {
    preferred_sets: ['长枪套装', '防御套装', '坦克套装'],
    stat_weights: {
      attack: 0.8,      // 低优先级 - 次要输出
      defense: 1.8,     // 最高优先级 - 主坦克属性
      health: 1.8,      // 最高优先级 - 生存能力
      crit: 1.0,        // 低优先级
      crit_damage: 1.0, // 低优先级
      element_damage: 1.0, // 低优先级
      speed: 0.8,       // 低优先级
    },
    description: '长柄武器，坦克型，扛伤输出兼具',
  },
  '医仙': {
    preferred_sets: ['治疗套装', '辅助套装', '生命套装'],
    stat_weights: {
      attack: 0.5,      // 最低优先级 - 几乎不需要
      defense: 1.2,     // 中等优先级 - 自保能力
      health: 1.8,      // 最高优先级 - 生存和治療量
      crit: 1.3,        // 中等优先级 - 治疗暴击
      crit_damage: 1.0, // 低优先级
      element_damage: 0.8, // 低优先级
      speed: 1.0,       // 中等优先级 - 施法速度
    },
    description: '辅助治疗，团队核心',
  },
  '拳师': {
    preferred_sets: ['拳法套装', '格斗套装', '近身套装'],
    stat_weights: {
      attack: 1.6,      // 高优先级 - 主要输出
      defense: 1.2,     // 中等优先级 - 近身需要
      health: 1.0,      // 中等优先级
      crit: 1.5,        // 高优先级
      crit_damage: 1.6, // 高优先级
      element_damage: 1.2, // 中等优先级
      speed: 1.8,       // 最高优先级 - 攻速至关重要
    },
    description: '近战格斗，高频率攻击',
  },
  '刺客': {
    preferred_sets: ['暗影套装', '潜行套装', '暴击套装'],
    stat_weights: {
      attack: 1.4,      // 高优先级
      defense: 0.5,     // 低优先级 - 玻璃大炮
      health: 0.5,      // 低优先级 - 高风险高回报
      crit: 2.0,        // 最高优先级 - 核心属性
      crit_damage: 2.0, // 最高优先级 - 一击必杀
      element_damage: 1.5, // 高优先级
      speed: 1.6,       // 高优先级 - 机动性
    },
    description: '高风险高回报，一击必杀',
  },
}

/**
 * 计算装备评分
 * @param {Object} equipment - 装备对象
 * @param {string} className - 职业名称
 * @returns {Object} 评分结果
 */
export function calculateScore(equipment, className = '通用') {
  const config = CLASS_CONFIGS[className] || CLASS_CONFIGS['通用']
  const weights = config.stat_weights

  // 1. 品质分
  const quality_score = QUALITY_SCORES[equipment.quality] || 10

  // 2. 属性分
  let stats_score = 0
  if (equipment.stats && Array.isArray(equipment.stats)) {
    for (const stat of equipment.stats) {
      const weight = weights[stat.name] || 0.5
      stats_score += (stat.value || 0) * weight
    }
  }

  // 3. 强化分
  const level_score = calculateLevelScore(equipment.level || 0)

  // 4. 套装加成
  const set_bonus = calculateSetBonus(equipment, config)

  // 5. 总分
  const total_score = quality_score + stats_score + level_score + set_bonus

  // 6. 生成建议
  const recommendation = generateRecommendation(equipment, total_score, config)

  return {
    total_score,
    quality_score,
    stats_score,
    level_score,
    set_bonus,
    recommendation,
    class_name: className,
  }
}

/**
 * 计算强化分
 */
function calculateLevelScore(level) {
  const base = level * 0.1 * 10
  const bonus = (level / 10) * 0.1 * 5
  return base + bonus
}

/**
 * 计算套装加成
 */
function calculateSetBonus(equipment, config) {
  if (!equipment.set_name) return 0

  if (config.preferred_sets && config.preferred_sets.includes(equipment.set_name)) {
    return 20 // 推荐套装
  }

  return 5 // 普通套装
}

/**
 * 生成培养建议
 */
function generateRecommendation(equipment, totalScore, config) {
  const suggestions = []

  // 根据总分
  if (totalScore >= 200) {
    suggestions.push('极品装备，建议优先培养')
  } else if (totalScore >= 150) {
    suggestions.push('优秀装备，值得培养')
  } else if (totalScore >= 100) {
    suggestions.push('普通装备，过渡使用')
  } else {
    suggestions.push('建议替换')
  }

  // 根据品质
  if (equipment.quality >= 4) {
    suggestions.push('高品质装备，建议保留')
  } else if (equipment.quality <= 2) {
    suggestions.push('品质较低，可作为强化材料')
  }

  // 根据强化等级
  if (equipment.level >= 10) {
    suggestions.push('已高度强化，建议继续使用')
  } else if (equipment.level === 0 && equipment.quality >= 3) {
    suggestions.push('未强化，建议投入资源')
  }

  // 根据套装
  if (equipment.set_name && config.preferred_sets?.includes(equipment.set_name)) {
    suggestions.push('套装契合度高，推荐作为毕业装备')
  }

  return suggestions.join('；')
}

/**
 * 对比两件装备
 */
export function compareEquipment(eq1, eq2, className = '通用') {
  const score1 = calculateScore(eq1, className)
  const score2 = calculateScore(eq2, className)

  const diff = score1.total_score - score2.total_score

  return {
    equipment1: {
      name: eq1.name,
      score: score1.total_score,
      details: score1,
    },
    equipment2: {
      name: eq2.name,
      score: score2.total_score,
      details: score2,
    },
    better: diff > 0 ? eq1.name : eq2.name,
    score_diff: Math.abs(diff),
  }
}

/**
 * 批量评分
 */
export function bulkScore(equipmentList, className = '通用') {
  return equipmentList.map(eq => ({
    ...eq,
    scoreData: calculateScore(eq, className),
  }))
}
