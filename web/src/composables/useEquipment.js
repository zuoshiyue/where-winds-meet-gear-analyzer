/**
 * 装备管理 Composable
 */

import { ref } from 'vue'
import * as storage from '../utils/storage'
import { calculateScore } from '../utils/scorer'

export function useEquipment() {
  const equipmentList = ref([])
  const loading = ref(false)
  const error = ref(null)

  /**
   * 加载装备列表
   */
  async function loadEquipment() {
    loading.value = true
    error.value = null
    
    try {
      const list = await storage.getAllEquipment()
      // 添加评分
      equipmentList.value = list.map(eq => ({
        ...eq,
        score: calculateScore(eq).total_score,
      }))
    } catch (err) {
      error.value = err.message
      console.error('加载装备失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 添加装备
   */
  async function addEquipment(equipment) {
    try {
      const eq = await storage.addEquipment(equipment)
      equipmentList.value.push({
        ...eq,
        score: calculateScore(eq).total_score,
      })
      return eq
    } catch (err) {
      console.error('添加装备失败:', err)
      throw err
    }
  }

  /**
   * 批量添加装备
   */
  async function addEquipments(equipments) {
    try {
      const results = await storage.addEquipments(equipments)
      for (const eq of results) {
        equipmentList.value.push({
          ...eq,
          score: calculateScore(eq).total_score,
        })
      }
      return results
    } catch (err) {
      console.error('批量添加装备失败:', err)
      throw err
    }
  }

  /**
   * 更新装备
   */
  async function updateEquipment(id, updates) {
    try {
      const updated = await storage.updateEquipment(id, updates)
      if (updated) {
        const index = equipmentList.value.findIndex(eq => eq.id === id)
        if (index !== -1) {
          equipmentList.value[index] = {
            ...updated,
            score: calculateScore(updated).total_score,
          }
        }
      }
      return updated
    } catch (err) {
      console.error('更新装备失败:', err)
      throw err
    }
  }

  /**
   * 删除装备
   */
  async function deleteEquipment(id) {
    try {
      await storage.deleteEquipment(id)
      equipmentList.value = equipmentList.value.filter(eq => eq.id !== id)
    } catch (err) {
      console.error('删除装备失败:', err)
      throw err
    }
  }

  /**
   * 清空所有装备
   */
  async function clearAll() {
    try {
      await storage.clearAllEquipment()
      equipmentList.value = []
    } catch (err) {
      console.error('清空装备失败:', err)
      throw err
    }
  }

  /**
   * 获取装备详情
   */
  function getEquipmentById(id) {
    return equipmentList.value.find(eq => eq.id === id)
  }

  /**
   * 导出 CSV
   */
  async function exportCSV() {
    const data = await storage.exportData()
    return data
  }

  /**
   * 导入数据
   */
  async function importData(jsonString) {
    await loadEquipment()
  }

  /**
   * 获取统计数据
   */
  async function getStatistics() {
    return await storage.getStatistics()
  }

  return {
    equipmentList,
    loading,
    error,
    loadEquipment,
    addEquipment,
    addEquipments,
    updateEquipment,
    deleteEquipment,
    clearAll,
    getEquipmentById,
    exportCSV,
    importData,
    getStatistics,
  }
}
