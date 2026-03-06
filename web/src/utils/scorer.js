/**
 * 装备评分模块
 * 根据燕云十六声武器心法流派计算装备评分
 * 
 * 参考项目:
 * - 燕云伤害模拟器：https://kaph404.github.io/Yanyun-calculator/
 * - 燕云十六声攻略站：https://yy16s.github.io/
 * - 玩家社区整理：《燕云十六声》全主流流派双武配置总表 (2026.03 版)
 * 
 * 核心属性:
 * - 会心率 (暴击率) - 基准伤害 150%
 * - 会心伤害 (爆伤) - 默认 150%
 * - 会意率 - 特殊属性
 * - 会意伤害 - 默认 135%
 * - 精准率
 * 
 * 流派分类 (玩家通用 - 2026.03 版):
 * - 破竹·鸢 (剑 + 扇) - T0 极致爆发
 * - 牵丝·玉 (弓 + 伞) - T0 远程风筝
 * - 破竹·风 (剑 + 刀) - T0.5 高频吸血
 * - 破竹·尘 (剑 + 笛) - T0.5 强力控制
 * - 鸣金·影 (枪 + 剑) - T0.5 流血爆发
 * - 鸣金·虹 (枪 + 弓) - T1 中距离拉扯
 * - 裂石·威 (重剑 + 盾) - T1 绝对防御
 * - 裂石·钧 (重剑 + 锤) - T1 超级破韧
 * - 奇门·幻 (扇 + 笛) - T1 诡异身法
 * - 游龙·水 (刀 + 扇) - T2 高机动
 */

// 品质基础分
const QUALITY_SCORES = {
  1: 10,  // 白色
  2: 30,  // 绿色
  3: 60,  // 蓝色
  4: 100, // 紫色
  5: 150, // 金色
}

// 默认属性权重 (参考玩家通用标准)
const DEFAULT_STAT_WEIGHTS = {
  attack: 1.0,        // 攻击 (外功)
  defense: 0.8,       // 防御
  health: 0.7,        // 生命
  crit: 1.5,          // 会心率 (暴击)
  crit_damage: 1.5,   // 会心伤害 (爆伤)
  element_damage: 1.3, // 元素伤害
  speed: 1.0,         // 速度/攻速
  precision: 1.0,     // 精准率
}

/**
 * 武器/心法流派配置
 * 
 * 燕云十六声采用自由流派系统，由武器和心法决定玩法
 * 根据玩家社区整理的《全主流流派双武配置总表》(2026.03 版)
 * 
 * 参考：https://kaph404.github.io/Yanyun-calculator/
 */
const FLOW_CONFIGS = {
  '通用': {
    preferred_sets: [],
    stat_weights: DEFAULT_STAT_WEIGHTS,
    description: '通用配置，适合所有流派',
  },
  
  // ===== T0 梯队 =====
  '破竹·鸢': {
    preferred_sets: ['爆发套装', '疾风套装', '剑气套装'],
    stat_weights: {
      attack: 1.8,        // 极致攻击
      defense: 0.6,
      health: 0.6,
      crit: 2.0,          // 会心率 - 核心属性
      crit_damage: 2.0,   // 会心伤害 - 核心属性
      element_damage: 1.5,
      speed: 1.8,         // 高频位移
      precision: 1.3,
    },
    description: 'T0 极致爆发/无敌帧 - 剑 + 扇，竞速本必备',
  },
  
  '牵丝·玉': {
    preferred_sets: ['远程套装', '增益套装', '护盾套装'],
    stat_weights: {
      attack: 1.6,
      defense: 1.0,
      health: 1.2,
      crit: 1.8,
      crit_damage: 1.8,
      element_damage: 1.4,
      speed: 1.3,
      precision: 1.5,     // 远程精准
    },
    description: 'T0 远程风筝/团队增益 - 弓 + 伞，单刷最安全',
  },
  
  // ===== T0.5 梯队 =====
  '破竹·风': {
    preferred_sets: ['吸血套装', '连斩套装', '持续输出套装'],
    stat_weights: {
      attack: 1.7,
      defense: 0.8,
      health: 1.0,        // 吸血需要一定生存
      crit: 1.9,
      crit_damage: 1.9,
      element_damage: 1.4,
      speed: 1.9,         // 高频攻击
      precision: 1.3,
    },
    description: 'T0.5 高频吸血/持续压制 - 剑 + 刀，站桩输出强',
  },
  
  '破竹·尘': {
    preferred_sets: ['控制套装', '辅助套装', '破防套装'],
    stat_weights: {
      attack: 1.4,
      defense: 1.0,
      health: 1.0,
      crit: 1.6,
      crit_damage: 1.6,
      element_damage: 1.5,
      speed: 1.4,
      precision: 1.2,
    },
    description: 'T0.5 强力控制/团队辅助 - 剑 + 笛，高难本必备',
  },
  
  '鸣金·影': {
    preferred_sets: ['流血套装', '近战套装', '爆发套装'],
    stat_weights: {
      attack: 1.7,
      defense: 0.7,
      health: 0.7,
      crit: 1.9,
      crit_damage: 1.9,
      element_damage: 1.4,
      speed: 1.6,
      precision: 1.3,
    },
    description: 'T0.5 流血爆发/近战缠斗 - 枪 + 剑，高爆发数字',
  },
  
  // ===== T1 梯队 =====
  '鸣金·虹': {
    preferred_sets: ['通用套装', '新手套装', '平衡套装'],
    stat_weights: {
      attack: 1.5,
      defense: 0.9,
      health: 0.9,
      crit: 1.7,
      crit_damage: 1.7,
      element_damage: 1.3,
      speed: 1.4,
      precision: 1.2,
    },
    description: 'T1 中距离拉扯/新手友好 - 枪 + 弓，开荒体验极佳',
  },
  
  '裂石·威': {
    preferred_sets: ['防御套装', '格挡套装', '反击套装'],
    stat_weights: {
      attack: 1.2,
      defense: 1.8,        // 核心属性
      health: 1.5,         // 核心属性
      crit: 1.3,
      crit_damage: 1.3,
      element_damage: 1.0,
      speed: 0.9,
      precision: 1.0,
    },
    description: 'T1 绝对防御/反击输出 - 重剑 + 盾，生存率最高',
  },
  
  '裂石·钧': {
    preferred_sets: ['破韧套装', '眩晕套装', '控制套装'],
    stat_weights: {
      attack: 1.4,
      defense: 1.6,
      health: 1.4,
      crit: 1.4,
      crit_damage: 1.4,
      element_damage: 1.1,
      speed: 1.0,
      precision: 1.1,
    },
    description: 'T1 超级破韧/眩晕控制 - 重剑 + 锤，克制巨型 BOSS',
  },
  
  '奇门·幻': {
    preferred_sets: ['异常套装', '中毒套装', '控制套装'],
    stat_weights: {
      attack: 1.3,
      defense: 0.9,
      health: 0.9,
      crit: 1.5,
      crit_damage: 1.5,
      element_damage: 1.8,  // 异常状态核心
      speed: 1.5,
      precision: 1.2,
    },
    description: 'T1 诡异身法/异常状态 - 扇 + 笛，PVP 强势',
  },
  
  // ===== T2 梯队 =====
  '游龙·水': {
    preferred_sets: ['机动套装', '闪避套装', '反击套装'],
    stat_weights: {
      attack: 1.5,
      defense: 0.7,
      health: 0.7,
      crit: 1.7,
      crit_damage: 1.7,
      element_damage: 1.3,
      speed: 2.0,           // 极致速度
      precision: 1.3,
    },
    description: 'T2 高机动/闪避反击 - 刀 + 扇，适合高手秀操作',
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
    'T0 梯队': ['破竹·鸢', '牵丝·玉'],
    'T0.5 梯队': ['破竹·风', '破竹·尘', '鸣金·影'],
    'T1 梯队': ['鸣金·虹', '裂石·威', '裂石·钧', '奇门·幻'],
    'T2 梯队': ['游龙·水'],
    '其他': ['通用'],
  }
}
