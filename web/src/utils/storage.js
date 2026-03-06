/**
 * 本地存储模块
 * 使用 localforage (IndexedDB) 存储装备数据
 */

import localforage from 'localforage'

// 初始化数据库
const db = localforage.createInstance({
  name: 'WhereWindsGear',
  storeName: 'equipment',
  description: '燕云十六声装备数据',
})

/**
 * 获取所有装备
 */
export async function getAllEquipment() {
  const keys = await db.keys()
  const equipments = await Promise.all(
    keys.map(key => db.getItem(key))
  )
  return equipments.filter(eq => eq !== null)
}

/**
 * 根据 ID 获取装备
 */
export async function getEquipmentById(id) {
  return await db.getItem(id.toString())
}

/**
 * 添加装备
 */
export async function addEquipment(equipment) {
  const id = await generateId()
  const eq = {
    ...equipment,
    id,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }
  await db.setItem(id.toString(), eq)
  return eq
}

/**
 * 批量添加装备
 */
export async function addEquipments(equipments) {
  const results = []
  for (const eq of equipments) {
    const result = await addEquipment(eq)
    results.push(result)
  }
  return results
}

/**
 * 更新装备
 */
export async function updateEquipment(id, updates) {
  const existing = await db.getItem(id.toString())
  if (!existing) return null

  const updated = {
    ...existing,
    ...updates,
    updated_at: new Date().toISOString(),
  }
  await db.setItem(id.toString(), updated)
  return updated
}

/**
 * 删除装备
 */
export async function deleteEquipment(id) {
  await db.removeItem(id.toString())
}

/**
 * 清空所有装备
 */
export async function clearAllEquipment() {
  await db.clear()
}

/**
 * 获取装备数量
 */
export async function getEquipmentCount() {
  const keys = await db.keys()
  return keys.length
}

/**
 * 生成唯一 ID
 */
async function generateId() {
  const timestamp = Date.now()
  const random = Math.floor(Math.random() * 1000)
  return `${timestamp}-${random}`
}

/**
 * 导出所有数据为 JSON
 */
export async function exportData() {
  const equipments = await getAllEquipment()
  return JSON.stringify(equipments, null, 2)
}

/**
 * 从 JSON 导入数据
 */
export async function importData(jsonString) {
  const equipments = JSON.parse(jsonString)
  if (!Array.isArray(equipments)) {
    throw new Error('无效的数据格式')
  }

  const results = []
  for (const eq of equipments) {
    const result = await addEquipment(eq)
    results.push(result)
  }
  return results
}

/**
 * 获取统计数据
 */
export async function getStatistics() {
  const equipments = await getAllEquipment()

  const stats = {
    total: equipments.length,
    by_quality: {},
    by_type: {},
    avg_level: 0,
    total_score: 0,
  }

  let totalLevel = 0

  for (const eq of equipments) {
    // 按品质统计
    const quality = eq.quality || 1
    stats.by_quality[quality] = (stats.by_quality[quality] || 0) + 1

    // 按类型统计
    const type = eq.type || '未知'
    stats.by_type[type] = (stats.by_type[type] || 0) + 1

    // 累计等级
    totalLevel += (eq.level || 0)
  }

  // 平均等级
  stats.avg_level = equipments.length > 0 
    ? (totalLevel / equipments.length).toFixed(1) 
    : 0

  return stats
}
