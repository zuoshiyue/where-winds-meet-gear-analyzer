/**
 * 装备评分模块
 * 根据燕云十六声武器心法流派计算装备评分
 * 
 * 燕云十六声是武器心法决定的流派制度，非固定职业
 * 参考：https://wwm-db.com/zh/
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
  attack: 1.0,        // 攻击
  defense: 0.8,       // 防御
  health: 0.7,        // 生命
  crit: 1.5,          // 暴击
  crit_damage: 1.5,   // 爆伤
  element_damage: 1.3, // 元素伤害
  speed: 1.0,         // 速度/攻速
}

/**
 * 武器/心法流派配置
 * 
 * 燕云十六声采用自由流派系统，由武器和心法决定玩法
 * 参考玩家通用命名和 wwm-db.com 数据
 * 
 * 玩家通用命名：
 * - 无名 (基础)、九剑 (剑)、九枪 (枪)、双刀 (双刃)
 * - 唐横刀 (刀)、裂石钧 (坦克)、伞扇 (伞)
 * - 嗟夫 (特殊武器) 等
 */
const FLOW_CONFIGS = {
  '通用': {
    preferred_sets: [],
    stat_weights: DEFAULT_STAT_WEIGHTS,
    description: '通用配置，适合所有流派',
  },
  
  // ===== 输出流派 =====
  '九剑·输出': {
    preferred_sets: ['剑心套装', '疾风套装', '暴击套装'],
    stat_weights: {
      attack: 1.5,
      defense: 1.0,
      health: 0.8,
      crit: 1.8,
      crit_damage: 1.8,
      element_damage: 1.3,
      speed: 1.5,
    },
    description: '九剑输出，攻守兼备，高机动性',
  },
  
  '九枪·输出': {
    preferred_sets: ['长枪套装', '破军套装', '暴击套装'],
    stat_weights: {
      attack: 1.6,
      defense: 0.8,
      health: 0.7,
      crit: 1.7,
      crit_damage: 1.9,
      element_damage: 1.4,
      speed: 1.3,
    },
    description: '九枪输出，长柄范围，高爆发',
  },
  
  '双刀·刺客': {
    preferred_sets: ['暗影套装', '潜行套装', '暴击套装'],
    stat_weights: {
      attack: 1.4,
      defense: 0.5,
      health: 0.5,
      crit: 2.0,
      crit_damage: 2.0,
      element_damage: 1.5,
      speed: 1.6,
    },
    description: '双刀刺客，高风险高回报，一击必杀',
  },
  
  '唐横刀·狂战': {
    preferred_sets: ['霸刀套装', '铁血套装', '强攻套装'],
    stat_weights: {
      attack: 1.8,
      defense: 0.6,
      health: 0.6,
      crit: 1.6,
      crit_damage: 1.9,
      element_damage: 1.4,
      speed: 1.2,
    },
    description: '唐横刀狂战，极致输出，快速击倒',
  },
  
  // ===== 坦克流派 =====
  '九枪·坦克': {
    preferred_sets: ['防御套装', '坦克套装', '生命套装'],
    stat_weights: {
      attack: 0.8,
      defense: 1.8,
      health: 1.8,
      crit: 1.0,
      crit_damage: 1.0,
      element_damage: 1.0,
      speed: 0.8,
    },
    description: '九枪坦克，扛伤输出兼具',
  },
  
  '裂石钧·防御': {
    preferred_sets: ['玄钧套装', '防御套装', '反震套装'],
    stat_weights: {
      attack: 0.9,
      defense: 1.7,
      health: 1.5,
      crit: 1.2,
      crit_damage: 1.2,
      element_damage: 1.1,
      speed: 1.0,
    },
    description: '裂石钧防御，以守为攻，反弹伤害',
  },
  
  // ===== 辅助流派 =====
  '医仙·治疗': {
    preferred_sets: ['治疗套装', '辅助套装', '生命套装'],
    stat_weights: {
      attack: 0.5,
      defense: 1.2,
      health: 1.8,
      crit: 1.3,
      crit_damage: 1.0,
      element_damage: 0.8,
      speed: 1.0,
    },
    description: '医仙治疗，团队核心，救死扶伤',
  },
  
  '伞扇·辅助': {
    preferred_sets: ['音律套装', '辅助套装', '控制套装'],
    stat_weights: {
      attack: 0.8,
      defense: 1.0,
      health: 1.5,
      crit: 1.2,
      crit_damage: 1.0,
      element_damage: 1.3,
      speed: 1.2,
    },
    description: '伞扇辅助，控制增益，团队支援',
  },
  
  // ===== 特殊流派 =====
  '无名·基础': {
    preferred_sets: ['无名套装', '通用套装'],
    stat_weights: {
      attack: 1.0,
      defense: 1.0,
      health: 1.0,
      crit: 1.0,
      crit_damage: 1.0,
      element_damage: 1.0,
      speed: 1.0,
    },
    description: '无名基础，平衡发展，新手推荐',
  },
  
  '嗟夫·特殊': {
    preferred_sets: ['嗟夫套装', '特殊套装'],
    stat_weights: {
      attack: 1.3,
      defense: 0.9,
      health: 1.0,
      crit: 1.5,
      crit_damage: 1.5,
      element_damage: 1.4,
      speed: 1.3,
    },
    description: '嗟夫特殊，独特机制，灵活多变',
  },
}

/**
 * 计算装备评分
 * @param {Object} equipment - 装备对象
 * @param {string} flowName - 流派名称
 * @returns {Object} 评分结果
 */
export function calculateScore(equipment, flowName = '通用') {
  const config = FLOW_CONFIGS[flowName] || FLOW_CONFIGS['通用']
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
    flow_name: flowName,
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

  return suggestions.join(';')
}

/**
 * 对比两件装备
 */
export function compareEquipment(eq1, eq2, flowName = '通用') {
  const score1 = calculateScore(eq1, flowName)
  const score2 = calculateScore(eq2, flowName)

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
export function bulkScore(equipmentList, flowName = '通用') {
  return equipmentList.map(eq => ({
    ...eq,
    scoreData: calculateScore(eq, flowName),
  }))
}

/**
 * 获取所有可用流派
 */
export function getAvailableFlows() {
  return Object.keys(FLOW_CONFIGS).map(key => ({
    key,
    ...FLOW_CONFIGS[key],
  }))
}

/**
 * 获取流派分类
 */
export function getFlowCategories() {
  return {
    '输出流派': ['九剑·输出', '九枪·输出', '双刀·刺客', '唐横刀·狂战'],
    '坦克流派': ['九枪·坦克', '裂石钧·防御'],
    '辅助流派': ['医仙·治疗', '伞扇·辅助'],
    '特殊流派': ['无名·基础', '嗟夫·特殊'],
    '其他': ['通用'],
  }
}
