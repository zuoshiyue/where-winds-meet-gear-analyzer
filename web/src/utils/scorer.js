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

// 默认属性权重 (根据燕云工具数据文档更新 - 2026-03-06)
// 参考：https://gamemad.com/guide/362969
const DEFAULT_STAT_WEIGHTS = {
  attack: 1.0,        // 最大外功攻击 (基准)
  min_attack: 0.7,    // 最小外功攻击
  jin: 0.8,           // 劲 (转化为攻击)
  shi: 0.7,           // 势
  precision: 1.0,     // 精准率
  crit: 1.2,          // 会心率
  crit_damage: 1.2,   // 会意率
  element_damage: 1.0, // 属性攻击 (鸣金/裂石等)
  boss_damage: 1.3,   // 首领增伤 (毕业核心)
  skill_damage: 1.2,  // 武学增伤 (剑/刀/拳等)
  defense: 0.8,       // 防御
  health: 0.7,        // 生命
  speed: 1.0,         // 速度/攻速
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
   * 核心属性：最大外功攻击 > 精准率 > 会心率/会意率 > 最大鸣金攻击 > 剑武学增伤
   */
  '鸣金·虹': {
    preferred_sets: ['鸣金套装', '均衡套装', '远程套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.2,     // 精准率 95%+ (门槛属性)
      crit: 1.1,          // 会心率 38%+
      crit_damage: 1.1,   // 会意率 39%+
      element_damage: 1.0, // 鸣金攻击
      skill_damage: 1.2,  // 剑武学增伤
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      min_attack: 0.7,    // 最小外功攻击
      jin: 0.9,           // 劲 (转化为攻击)
      defense: 0.9,
      health: 0.9,
    },
    description: '中远程均衡输出 - 无名剑 + 无名枪，攻守兼备万金油',
  },
  
  /**
   * 鸣金·影 - 近战流血爆发
   * 武器：积矩九剑 + 九曲惊神枪
   * 毕业面板：外攻 3800+，精准 97%+，会心 45%+，会意 37%+，鸣金 850+
   * 核心属性：最大外功攻击 > 精准率 > 会心率/会意率 > 最大鸣金攻击 > 剑武学增伤
   */
  '鸣金·影': {
    preferred_sets: ['鸣金套装', '流血套装', '爆发套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.2,     // 精准率 97%+ (门槛属性)
      crit: 1.1,          // 会心率 45%+
      crit_damage: 1.1,   // 会意率 37%+
      element_damage: 1.0, // 鸣金攻击
      skill_damage: 1.2,  // 剑武学增伤
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      min_attack: 0.7,
      jin: 0.9,
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
   * 核心属性：最大外功攻击 > 精准率 > 会心率 > 最大裂石攻击 > 首领增伤
   */
  '裂石·威': {
    preferred_sets: ['裂石套装', '坦克套装', '减伤套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.3,     // 精准率 98%+ (门槛属性)
      crit: 1.2,          // 会心率 56%+
      element_damage: 1.0, // 裂石攻击
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      min_attack: 0.7,
      jin: 1.1,           // 劲 (物理核心)
      shi: 1.0,           // 势
      defense: 1.2,       // 坦克需要生存
      health: 1.1,
    },
    description: '坦克/近战输出 - 嗟夫刀 + 八方枪，团队前排',
  },
  
  /**
   * 裂石·钧 - 横刀/首领增伤
   * 武器：十方破阵 + 斩雪刀法
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，裂石 850+
   * 核心属性：最大外功攻击 > 精准率 > 会心率 > 最大裂石攻击 > 横刀/首领增伤
   */
  '裂石·钧': {
    preferred_sets: ['裂石套装', '横刀套装', '首领增伤套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.3,     // 精准率 98%+ (门槛属性)
      crit: 1.2,          // 会心率 70%+
      element_damage: 1.0, // 裂石攻击
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      skill_damage: 1.2,  // 横刀增伤
      min_attack: 0.7,
      jin: 1.1,
      shi: 1.0,
      defense: 1.0,
      health: 1.0,
    },
    description: '横刀/首领增伤 - 十方破阵 + 斩雪刀，克制巨型 BOSS',
  },
  
  // ===== 破竹流派 (3 个) =====
  
  /**
   * 破竹·风 - 近战高机动刺客
   * 武器：泥犁三垢 + 粟子游尘
   * 毕业面板：外攻 1700-3400，精准 98%+，会心 65%+，破竹 850+
   * 核心属性：最大外功攻击 > 精准率 > 会心率 > 最大破竹攻击 > 首领增伤
   */
  '破竹·风': {
    preferred_sets: ['破竹套装', '机动套装', '毒伤套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.3,     // 精准率 98%+ (门槛属性)
      crit: 1.2,          // 会心率 65%+
      element_damage: 1.0, // 破竹攻击
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      min_attack: 0.7,
      jin: 1.1,
      speed: 1.2,         // 高机动
      defense: 0.8,
      health: 0.8,
    },
    description: '近战高机动刺客 - 泥犁 + 粟子，专攻弱点',
  },
  
  /**
   * 破竹·鸢 - 全能型控制/输出 (版本之子)
   * 武器：天志垂象 + 千机锁天
   * 毕业面板：外攻 1800-3300，精准 98%+，会心率 75%+，破竹 850+
   * 核心属性：会心率 > 最大外功攻击 > 精准率 > 最大破竹攻击 > 拳甲增伤
   */
  '破竹·鸢': {
    preferred_sets: ['破竹套装', '控制套装', '霸体套装'],
    stat_weights: {
      crit: 1.5,          // 会心率 75%+ (核心)
      crit_damage: 1.4,   // 会意率 (核心)
      attack: 0.9,        // 最大外功攻击
      precision: 1.1,     // 精准率 98%+
      element_damage: 0.7, // 破竹攻击
      skill_damage: 1.2,  // 拳甲增伤
      boss_damage: 1.3,   // 首领增伤
      min_attack: 0.6,
      jin: 0.8,
      defense: 0.9,
      health: 0.9,
    },
    description: '全能型控制/输出 - 天志 + 千机，战场适应性强 (版本之子)',
  },
  
  /**
   * 破竹·尘 - 伞/首领增伤
   * 武器：醉梦游春 + 粟子行云
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，破竹 850+
   * 核心属性：最大外功攻击 > 精准率 > 会心率 > 最大破竹攻击 > 伞/首领增伤
   */
  '破竹·尘': {
    preferred_sets: ['破竹套装', '伞套装', '首领增伤套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.3,     // 精准率 98%+ (门槛属性)
      crit: 1.2,          // 会心率 70%+
      element_damage: 1.0, // 破竹攻击
      boss_damage: 1.3,   // 首领增伤 (毕业核心)
      skill_damage: 1.2,  // 伞增伤
      min_attack: 0.7,
      jin: 1.0,
      speed: 1.1,
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
   * 核心属性：最大鸣金攻击 > 会心率 > 最大牵丝攻击 > 玩家增伤
   */
  '牵丝·霖': {
    preferred_sets: ['牵丝套装', '治疗套装', '增益套装'],
    stat_weights: {
      element_damage: 1.2, // 鸣金攻击 (影响治疗)
      crit: 0.8,          // 会心率 75%+
      crit_damage: 0.6,   // 会意率
      attack: 0.6,        // 外功攻击 (次要)
      min_attack: 0.5,
      jin: 0.3,           // 劲 (生存向)
      shi: 0.5,
      player_damage: 1.0, // 玩家增伤 (PVP)
      defense: 1.0,
      health: 1.1,        // 治疗需要一定生存
    },
    description: '纯治疗辅助 - 明川药典 + 千香蛊，团队生存保障',
  },
  
  /**
   * 牵丝·玉 - 散武学增伤
   * 武器：九重春色 + 青山执笔
   * 毕业面板：外攻 1700-3300，精准 98%+，会心 70%+，牵丝 850+
   * 核心属性：最大外功攻击 > 精准率 > 会心率 > 最大牵丝攻击 > 散武学增伤
   */
  '牵丝·玉': {
    preferred_sets: ['牵丝套装', '散武学套装', '增伤套装'],
    stat_weights: {
      attack: 1.0,        // 最大外功攻击 (基准)
      precision: 1.1,     // 精准率 98%+
      crit: 1.2,          // 会心率 70%+
      element_damage: 1.0, // 牵丝攻击
      skill_damage: 1.2,  // 散武学增伤
      min_attack: 0.6,
      jin: 0.8,
      shi: 0.7,
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
 * 计算装备推荐度（简易评分公式）
 * 装备推荐度 = 有效词条数 × 2 + 核心词条数 × 3 + (若为套装部件+5)
 * 
 * 分数解读：
 * - 8 分以下：过渡装备
 * - 8-12 分：优质散件
 * - 12 分以上：毕业候选
 */
export function calculateRecommendationScore(equipment, flow = '通用') {
  const weights = getStatWeights(flow)
  
  let validStats = 0  // 有效词条数 (权重≥0.8)
  let coreStats = 0   // 核心词条数 (权重≥1.2)
  
  // 统计词条
  if (equipment.stats && Array.isArray(equipment.stats)) {
    equipment.stats.forEach(stat => {
      const weight = weights[stat.type] || 0.5
      if (weight >= 1.2) {
        coreStats++
        validStats++
      } else if (weight >= 0.8) {
        validStats++
      }
    })
  }
  
  // 计算推荐度分数
  let score = validStats * 2 + coreStats * 3
  
  // 套装部件加分
  if (equipment.set_name) {
    score += 5
  }
  
  // 评级
  let grade = '过渡装备'
  if (score >= 12) grade = '毕业候选'
  else if (score >= 8) grade = '优质散件'
  
  return {
    score,
    validStats,
    coreStats,
    grade,
    isSet: !!equipment.set_name,
  }
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
