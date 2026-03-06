/**
 * 装备数据解析模块
 * 从 OCR 识别结果中提取装备信息
 */

/**
 * 从文本中解析装备数据
 * @param {string} text - OCR 识别的文本
 * @param {string} sourceFile - 源文件名
 * @returns {Object|null} 装备对象
 */
export function parseEquipmentFromText(text, sourceFile = '') {
  if (!text) return null

  const equipment = {
    name: '',
    type: '',
    quality: 1,
    level: 0,
    set_name: '',
    stats: [],
    screenshot_path: sourceFile,
    notes: '',
  }

  const lines = text.split('\n').filter(line => line.trim())

  for (const line of lines) {
    const trimmed = line.trim()

    // 尝试解析装备名称 (通常是第一行，包含"装备"或直接是名称)
    if (!equipment.name) {
      const nameMatch = trimmed.match(/(.+?)(?:装备|武器|防具|饰品)?$/)
      if (nameMatch && nameMatch[1].length >= 2 && nameMatch[1].length <= 20) {
        equipment.name = nameMatch[1].trim()
      }
    }

    // 解析装备类型
    if (trimmed.includes('武器') || trimmed.includes('剑') || trimmed.includes('刀')) {
      equipment.type = '武器'
    } else if (trimmed.includes('防具') || trimmed.includes('甲') || trimmed.includes('盔')) {
      equipment.type = '防具'
    } else if (trimmed.includes('饰品') || trimmed.includes('项链') || trimmed.includes('戒指')) {
      equipment.type = '饰品'
    }

    // 解析品质 (从颜色关键词或星星数量)
    if (trimmed.includes('金色') || trimmed.includes('传说')) {
      equipment.quality = 5
    } else if (trimmed.includes('紫色') || trimmed.includes('史诗')) {
      equipment.quality = 4
    } else if (trimmed.includes('蓝色') || trimmed.includes('稀有')) {
      equipment.quality = 3
    } else if (trimmed.includes('绿色') || trimmed.includes('优秀')) {
      equipment.quality = 2
    } else if (trimmed.includes('白色') || trimmed.includes('普通')) {
      equipment.quality = 1
    }

    // 解析强化等级 (+数字)
    const levelMatch = trimmed.match(/\+(\d+)/)
    if (levelMatch) {
      equipment.level = parseInt(levelMatch[1])
    }

    // 解析套装名称
    if (trimmed.includes('套装') || trimmed.includes('套')) {
      const setMatch = trimmed.match(/(.+?)(?:套装|套)/)
      if (setMatch) {
        equipment.set_name = setMatch[1].trim() + '套装'
      }
    }

    // 解析属性 (数字 + 属性名)
    const statMatch = trimmed.match(/(\d+(?:\.\d+)?)\s*(攻击 | 防御 | 生命 | 暴击 | 爆伤 | 元素|速度|Strength|Defense|Health|Crit)/i)
    if (statMatch) {
      const value = parseFloat(statMatch[1])
      const statName = mapStatName(statMatch[2])
      if (statName) {
        equipment.stats.push({
          name: statName,
          value: value,
        })
      }
    }
  }

  // 如果没有识别到有效名称，返回 null
  if (!equipment.name || equipment.name.length < 2) {
    return null
  }

  return equipment
}

/**
 * 映射属性名称到标准名称
 */
function mapStatName(name) {
  const mapping = {
    '攻击': 'attack',
    '防御': 'defense',
    '生命': 'health',
    '暴击': 'crit',
    '爆伤': 'crit_damage',
    '元素': 'element_damage',
    '速度': 'speed',
    'Attack': 'attack',
    'Defense': 'defense',
    'Health': 'health',
    'Crit': 'crit',
  }
  return mapping[name] || name.toLowerCase()
}

/**
 * 批量解析装备
 */
export function parseMultipleEquipment(texts) {
  const equipments = []
  
  for (const text of texts) {
    const equipment = parseEquipmentFromText(text)
    if (equipment) {
      equipments.push(equipment)
    }
  }
  
  return equipments
}

/**
 * 验证装备数据
 */
export function validateEquipment(equipment) {
  const errors = []

  if (!equipment.name || equipment.name.length < 2) {
    errors.push('装备名称无效')
  }

  if (equipment.quality < 1 || equipment.quality > 5) {
    errors.push('品质值必须在 1-5 之间')
  }

  if (equipment.level < 0 || equipment.level > 20) {
    errors.push('强化等级异常')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}
