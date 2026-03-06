/**
 * 装备评分模块
 * 根据燕云十六声武器心法流派计算装备评分
 * 
 * 参考项目:
 * - 燕云伤害模拟器：https://kaph404.github.io/Yanyun-calculator/
 * - 燕云十六声攻略站：https://yy16s.github.io/
 * - 官方九大武学流派 (2026.02 版)
 * 
 * 核心属性:
 * - 会心率 (暴击率) - 基准伤害 150%
 * - 会心伤害 (爆伤) - 默认 150%
 * - 会意率 - 特殊属性
 * - 会意伤害 - 默认 135%
 * - 精准率 - 命中率 (毕业 95%+)
 * 
 * 官方九大武学流派 (2026.02 版):
 * - 鸣金·虹 (无名剑 + 无名枪) - 中远程均衡输出
 * - 鸣金·影 (积矩九剑 + 九曲惊神枪) - 近战流血爆发
 * - 裂石·威 (嗟夫刀 + 八方风雷枪) - 坦克/近战输出
 * - 裂石·钧 (十方破阵 + 斩雪刀法) - 横刀/首领增伤
 * - 破竹·风 (泥犁三垢 + 粟子游尘) - 近战高机动刺客
 * - 破竹·鸢 (天志垂象 + 千机锁天) - 全能型控制/输出
 * - 破竹·尘 (醉梦游春 + 粟子行云) - 伞/首领增伤
 * - 牵丝·霖 (明川药典 + 千香引魂蛊) - 纯治疗辅助
 * - 牵丝·玉 (九重春色 + 青山执笔) - 散武学增伤
 * 
 * 100 级毕业标准 (2026.02):
 * - 精准率：95%-98%+
 * - 会心率：38%-75%+ (流派不同)
 * - 会意率：37%-39%+
 * - 外功攻击：1600-3800+ (流派不同)
 */

// 品质基础分
const QUALITY_SCORES = {
  1: 10,  // 白色
  2: 30,  // 绿色
  3: 60,  // 蓝色
  4: 100, // 紫色
  5: 150, // 金色
}

// 默认属性权重 (参考官方标准)
const DEFAULT_STAT_WEIGHTS = {
  attack: 1.0,        // 外功攻击
  defense: 0.8,       // 防御
  health: 0.7,        // 生命
  crit: 1.5,          // 会心率
  crit_damage: 1.5,   // 会意伤害
  element_damage: 1.3, // 元素伤害
  speed: 1.0,         // 速度/攻速
  precision: 1.0,     // 精准率
}

/**
 * 武器/心法流派配置
 * 
 * 根据《燕云十六声》官方九大武学流派 (2026.02 版)
 * 包含武器组合、核心定位、毕业面板参考
 */
const FLOW_CONFIGS = {
  '通用': {
    preferred_sets: [],
    stat_weights: DEFAULT_STAT_WEIGHTS,
    description: '通用配置，适合所有流派',
  },
  
  // ===== 鸣金流派 (2 个) =====
  
  /**
   * 鸣金·虹 - 中远程均衡输出
   * 武器：无名剑法 + 无名枪法
   * 毕业面板：外攻 3800+，精准 95%+，会心 38%+，会意 39%+，鸣金 850+
   */
  '鸣金·虹': {
    preferred_sets: ['鸣金套装', '均衡套装', '远程套装'],
    stat_weights: {
      attack: 1.8,        // 核心属性 - 外功攻击
      precision: 1.6,     // 精准率 95%+
      crit: 1.5,          // 会心率 38%+
      crit_damage: 1.5,   // 会意率 39%+
      element_damage: 1.3, // 鸣金攻击
      speed: 1.2,
      defense: 0.9,
      health: 0.9,
    },
    description: '中远程均衡输出 - 无名剑 + 无名枪，攻守兼备万金油',
  },
  
  /**
   * 鸣金·影 - 近战流血爆发
   * 武器：积矩九剑 + 九曲惊神枪
   * 毕业面板：外攻 3800+，精准 97%+，会心 45%+，会意 37%+，鸣金 850+
   */
  '鸣金·影': {
    preferred_sets: ['鸣金套装', '流血套装', '爆发套装'],
    stat_weights: {
      attack: 1.8,        // 核心属性 - 外功攻击
      precision: 1.7,     // 精准率 97%+
      crit: 1.6,          // 会心率 45%+
      crit_damage: 1.5,   // 会意率 37%+
      element_damage: 1.3, // 鸣金攻击
      speed: 1.3,
      defense: 0.8,
      health: 0.8,
    },
    description: '近战流血爆发 - 九剑 + 九曲枪，节奏感极强',
  },
  
  // ===== 裂石流派 (2 个) =====
  
  /**
   * 裂石·威 - 坦克/近战输出
   * 武器：嗟夫刀法 + 八方风雷枪
   * 毕业面板：外攻 1600-3300，精准 98%+，会心 56%+，裂石 900+
   */
  '裂石·威': {
    preferred_sets: ['裂石套装', '坦克套装', '减伤套装'],
    stat_weights: {
      attack: 1.4,        // 外功攻击 1600-3300
      precision: 1.8,     // 精准率 98%+
      crit: 1.7,          // 会心率 56%+
      element_damage: 1.6, // 裂石攻击 900+
      defense: 1.5,       // 坦克需要生存
      health: 1.4,
      speed: 1.0,
    },
    description: '坦克/近战输出 - 嗟夫刀 + 八方枪，团队前排',
  },
  
  /**
   * 裂石·钧 - 横刀/首领增伤
   * 武器：十方破阵 + 斩雪刀法
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，裂石 850+
   */
  '裂石·钧': {
    preferred_sets: ['裂石套装', '横刀套装', '首领增伤套装'],
    stat_weights: {
      attack: 1.7,        // 外功攻击 1700-3300
      precision: 1.8,     // 精准率 98%+
      crit: 1.9,          // 会心率 70%+
      element_damage: 1.6, // 裂石攻击 850+
      defense: 1.2,
      health: 1.2,
      speed: 1.1,
    },
    description: '横刀/首领增伤 - 十方破阵 + 斩雪刀，克制巨型 BOSS',
  },
  
  // ===== 破竹流派 (3 个) =====
  
  /**
   * 破竹·风 - 近战高机动刺客
   * 武器：泥犁三垢 + 粟子游尘
   * 毕业面板：外攻 1700-3400，精准 98%+，会心 65%+，破竹 850+
   */
  '破竹·风': {
    preferred_sets: ['破竹套装', '机动套装', '毒伤套装'],
    stat_weights: {
      attack: 1.7,        // 外功攻击 1700-3400
      precision: 1.8,     // 精准率 98%+
      crit: 1.9,          // 会心率 65%+
      element_damage: 1.6, // 破竹攻击 850+
      speed: 1.8,         // 高机动
      defense: 0.7,
      health: 0.7,
    },
    description: '近战高机动刺客 - 泥犁 + 粟子，专攻弱点',
  },
  
  /**
   * 破竹·鸢 - 全能型控制/输出
   * 武器：天志垂象 + 千机锁天
   * 毕业面板：外攻 1800-3300，精准 98%+，会心 75%+，破竹 850+
   */
  '破竹·鸢': {
    preferred_sets: ['破竹套装', '控制套装', '霸体套装'],
    stat_weights: {
      crit: 2.0,          // 核心 - 会心率 75%+
      crit_damage: 2.0,   // 核心 - 会意率
      attack: 1.8,        // 外功攻击 1800-3300
      precision: 1.8,     // 精准率 98%+
      element_damage: 1.6, // 破竹攻击 850+
      speed: 1.6,
      defense: 0.9,
      health: 0.9,
    },
    description: '全能型控制/输出 - 天志 + 千机，战场适应性强',
  },
  
  /**
   * 破竹·尘 - 伞/首领增伤
   * 武器：醉梦游春 + 粟子行云
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，破竹 850+
   */
  '破竹·尘': {
    preferred_sets: ['破竹套装', '伞套装', '首领增伤套装'],
    stat_weights: {
      attack: 1.7,        // 外功攻击 1700-3300
      precision: 1.8,     // 精准率 98%+
      crit: 1.9,          // 会心率 70%+
      element_damage: 1.6, // 破竹攻击 850+
      speed: 1.5,
      defense: 1.0,
      health: 1.0,
    },
    description: '伞/首领增伤 - 醉梦游春 + 粟子行云，控制辅助',
  },
  
  // ===== 牵丝流派 (2 个) =====
  
  /**
   * 牵丝·霖 - 纯治疗辅助
   * 武器：明川药典 + 千香引魂蛊
   * 毕业面板：外攻 1700-3400，会心 75%+，牵丝 850+
   */
  '牵丝·霖': {
    preferred_sets: ['牵丝套装', '治疗套装', '增益套装'],
    stat_weights: {
      crit: 2.0,          // 会心率 75%+ (最高)
      element_damage: 1.8, // 牵丝攻击 850+
      attack: 1.5,        // 外功攻击 1700-3400
      precision: 1.3,
      speed: 1.4,
      defense: 1.0,
      health: 1.2,        // 治疗需要一定生存
    },
    description: '纯治疗辅助 - 明川药典 + 千香蛊，团队生存保障',
  },
  
  /**
   * 牵丝·玉 - 散武学增伤
   * 武器：九重春色 + 青山执笔
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，牵丝 850+
   */
  '牵丝·玉': {
    preferred_sets: ['牵丝套装', '散武学套装', '增伤套装'],
    stat_weights: {
      attack: 1.7,        // 外功攻击 1700-3300
      precision: 1.8,     // 精准率 98%+
      crit: 1.9,          // 会心率 70%+
      element_damage: 1.8, // 牵丝攻击 850+
      speed: 1.4,
      defense: 1.0,
      health: 1.1,
    },
    description: '散武学增伤 - 九重春色 + 青山执笔，输出辅助',
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
    '鸣金流派': ['鸣金·虹', '鸣金·影'],
    '裂石流派': ['裂石·威', '裂石·钧'],
    '破竹流派': ['破竹·风', '破竹·鸢', '破竹·尘'],
    '牵丝流派': ['牵丝·霖', '牵丝·玉'],
    '其他': ['通用'],
  }
}
