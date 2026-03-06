/**
 * 胚子评估模块
 * 评估装备胚子是否值得培养
 * 
 * 核心逻辑：
 * 1. 胚子 = 未强化的原始装备（只有 1 个基础词条）
 * 2. 叠音 = 装备强化过程（每次增加/提升词条）
 * 3. 预过滤 = 根据单词条质量判断是否值得投资
 */

import { FLOW_CONFIGS } from './scorer.js'

/**
 * 词条权重配置（基于伤害公式推导）
 * 权重值 = 该词条对最终伤害的期望提升百分比系数
 */
export const STAT_WEIGHTS_BY_FLOW = {
  // ===== 通用权重 =====
  '通用': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 0.8,
    '势': 0.7,
    '精准率': 1.0,
    '会心率': 1.2,
    '会意率': 1.2,
    '鸣金攻击': 0.9,
    '裂石攻击': 0.9,
    '破竹攻击': 0.9,
    '牵丝攻击': 0.9,
    '首领增伤': 1.3,
    '武学增伤': 1.2,
    '玩家增伤': 1.0,
    '外功伤害加成': 1.1,
    '属性伤害加成': 1.0,
  },
  
  // ===== 鸣金流派 =====
  '鸣金·虹': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 0.9, // 转化为攻击
    '势': 0.8,
    '精准率': 1.2, // 门槛属性
    '会心率': 1.1,
    '会意率': 1.1,
    '鸣金攻击': 1.0,
    '剑武学增伤': 1.2,
    '首领增伤': 1.3, // 毕业核心
  },
  '鸣金·影': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 0.9,
    '势': 0.8,
    '精准率': 1.2,
    '会心率': 1.1,
    '会意率': 1.1,
    '鸣金攻击': 1.0,
    '剑武学增伤': 1.2,
    '首领增伤': 1.3,
  },
  
  // ===== 裂石流派 =====
  '裂石·威': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 1.1, // 物理核心
    '势': 1.0,
    '精准率': 1.3, // 门槛属性
    '会心率': 1.2,
    '裂石攻击': 1.0,
    '首领增伤': 1.3,
  },
  '裂石·钧': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 1.1,
    '势': 1.0,
    '精准率': 1.3,
    '会心率': 1.2,
    '裂石攻击': 1.0,
    '横刀增伤': 1.3,
    '首领增伤': 1.3,
  },
  
  // ===== 破竹流派 =====
  '破竹·风': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 1.1,
    '势': 0.9,
    '精准率': 1.3,
    '会心率': 1.2,
    '破竹攻击': 1.0,
    '首领增伤': 1.3,
  },
  '破竹·鸢': {
    '最大外功攻击': 0.9,
    '最小外功攻击': 0.6,
    '劲': 0.8,
    '势': 0.7,
    '精准率': 1.1,
    '会心率': 1.5, // 核心
    '会意率': 1.4, // 核心
    '破竹攻击': 0.7,
    '拳甲增伤': 1.2,
    '首领增伤': 1.3,
  },
  '破竹·尘': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.7,
    '劲': 1.0,
    '势': 0.9,
    '精准率': 1.3,
    '会心率': 1.2,
    '破竹攻击': 1.0,
    '伞增伤': 1.2,
    '首领增伤': 1.3,
  },
  
  // ===== 牵丝流派 =====
  '牵丝·霖': {
    '最大外功攻击': 0.6,
    '最小外功攻击': 0.5,
    '劲': 0.3,
    '势': 0.5,
    '会心率': 0.8,
    '鸣金攻击': 1.2, // 影响治疗
    '牵丝攻击': 1.2,
    '玩家增伤': 1.0,
  },
  '牵丝·玉': {
    '最大外功攻击': 1.0,
    '最小外功攻击': 0.6,
    '劲': 0.8,
    '势': 0.7,
    '精准率': 1.1,
    '会心率': 1.2,
    '牵丝攻击': 1.0,
    '散武学增伤': 1.2,
  },
}

/**
 * 胚子评级标准
 * 根据单词条的权重值评定等级
 */
export const EMBRYO_RATINGS = {
  S: { minWeight: 1.3, label: '极品胚子', advice: '值得全力培养', color: '#FFD700' },
  A: { minWeight: 1.1, label: '优质胚子', advice: '值得培养', color: '#FF6B6B' },
  B: { minWeight: 0.9, label: '普通胚子', advice: '可作为过渡', color: '#4ECDC4' },
  C: { minWeight: 0.0, label: '较差胚子', advice: '建议分解', color: '#95A5A6' },
}

/**
 * 叠音配置
 */
export const DIEYIN_CONFIG = {
  maxLevels: 5, // 最大叠音次数
 词条上限：4, // 最终词条数量
 每叠音消耗：'叠音石', // 强化材料
}

/**
 * 评估胚子是否值得培养
 * @param {Object} embryo - 胚子数据 { statName, statValue, equipmentType, flow }
 * @returns {Object} 评估结果
 */
export function evaluateEmbryo(embryo) {
  const { statName, statValue, equipmentType, flow = '通用' } = embryo
  
  // 获取该流派的词条权重
  const weights = STAT_WEIGHTS_BY_FLOW[flow] || STAT_WEIGHTS_BY_FLOW['通用']
  const weight = weights[statName] || 0.5
  
  // 计算胚子评分
  const embryoScore = statValue * weight
  
  // 确定评级
  let rating = 'C'
  let ratingInfo = EMBRYO_RATINGS['C']
  
  if (weight >= EMBRYO_RATINGS.S.minWeight) {
    rating = 'S'
    ratingInfo = EMBRYO_RATINGS.S
  } else if (weight >= EMBRYO_RATINGS.A.minWeight) {
    rating = 'A'
    ratingInfo = EMBRYO_RATINGS.A
  } else if (weight >= EMBRYO_RATINGS.B.minWeight) {
    rating = 'B'
    ratingInfo = EMBRYO_RATINGS.B
  }
  
  // 计算期望最终评分（假设完美叠音）
  const expectedFinalScore = embryoScore * 4 // 假设 4 词条完美
  
  // 判断是否值得培养
  const worthCultivating = rating === 'S' || rating === 'A'
  
  return {
    rating, // S/A/B/C
    label: ratingInfo.label,
    advice: ratingInfo.advice,
    color: ratingInfo.color,
    embryoScore: Math.round(embryoScore),
    weight,
    worthCultivating,
    expectedFinalScore: Math.round(expectedFinalScore),
    analysis: generateEmbryoAnalysis(embryo, weight, rating),
  }
}

/**
 * 生成胚子分析文案
 */
function generateEmbryoAnalysis(embryo, weight, rating) {
  const { statName, statValue, flow } = embryo
  
  const analyses = {
    S: `${statName} +${statValue} 是${flow}流派的核心属性，权重${weight.toFixed(2)}，极品胚子！建议全力培养至满级。`,
    A: `${statName} +${statValue} 是${flow}流派的优质属性，权重${weight.toFixed(2)}，值得培养。`,
    B: `${statName} +${statValue} 对于${flow}流派收益一般，权重${weight.toFixed(2)}，可作为过渡装备使用。`,
    C: `${statName} +${statValue} 不是${flow}流派的核心属性，权重${weight.toFixed(2)}，建议分解或作为狗粮。`,
  }
  
  return analyses[rating] || analyses.B
}

/**
 * 计算叠音后的装备评分
 * @param {Array} stats - 词条数组 [{statName, statValue}, ...]
 * @param {String} flow - 流派
 * @returns {Object} 评分结果
 */
export function calculateDieyinScore(stats, flow = '通用') {
  const weights = STAT_WEIGHTS_BY_FLOW[flow] || STAT_WEIGHTS_BY_FLOW['通用']
  
  let totalScore = 0
  let validStats = 0
  let coreStats = 0
  
  const statDetails = stats.map(stat => {
    const weight = weights[stat.statName] || 0.5
    const score = stat.statValue * weight
    totalScore += score
    validStats += (weight >= 0.8 ? 1 : 0)
    coreStats += (weight >= 1.2 ? 1 : 0)
    
    return {
      ...stat,
      weight,
      score: Math.round(score),
      isCore: weight >= 1.2,
      isValid: weight >= 0.8,
    }
  })
  
  // 计算推荐度分数
  const recommendationScore = validStats * 2 + coreStats * 3
  
  // 评级
  let grade = '过渡'
  if (recommendationScore >= 12) grade = '毕业候选'
  else if (recommendationScore >= 8) grade = '优质散件'
  
  return {
    totalScore: Math.round(totalScore),
    recommendationScore,
    grade,
    validStats,
    coreStats,
    statCount: stats.length,
    statDetails,
  }
}

/**
 * 对比叠音前后评分变化
 * @param {Object} before - 叠音前数据
 * @param {Object} after - 叠音后数据
 * @returns {Object} 对比结果
 */
export function compareDieyin(before, after) {
  const scoreDiff = after.totalScore - before.totalScore
  const changePercent = ((scoreDiff / before.totalScore) * 100).toFixed(1)
  
  const isGood = scoreDiff > 0
  const isGreat = scoreDiff > before.totalScore * 0.3 // 提升超过 30%
  
  let advice = ''
  if (isGreat) {
    advice = '✨ 完美叠音！继续培养！'
  } else if (isGood) {
    advice = '✓ 正常提升，可以继续'
  } else {
    advice = '⚠️ 提升不理想，考虑是否继续'
  }
  
  return {
    scoreDiff,
    changePercent,
    isGood,
    isGreat,
    advice,
    before,
    after,
  }
}

/**
 * 判断是否值得继续叠音
 * @param {Object} current - 当前装备状态
 * @param {Number} currentLevel - 当前叠音等级
 * @param {String} flow - 流派
 * @returns {Object} 建议
 */
export function shouldContinueDieyin(current, currentLevel, flow) {
  const { grade, coreStats, validStats } = current
  
  // 已经是毕业装备
  if (grade === '毕业候选' && currentLevel >= 3) {
    return {
      continue: false,
      reason: '已达到毕业标准，可以停止',
      confidence: 'high',
    }
  }
  
  // 核心词条数量足够
  if (coreStats >= 2 && currentLevel >= 3) {
    return {
      continue: false,
      reason: '核心词条已达标，见好就收',
      confidence: 'medium',
    }
  }
  
  // 有效词条太少
  if (validStats === 0 && currentLevel >= 2) {
    return {
      continue: false,
      reason: '有效词条太少，建议止损',
      confidence: 'high',
    }
  }
  
  // 继续培养
  return {
    continue: true,
    reason: '还有提升空间，继续叠音',
    confidence: 'medium',
  }
}
