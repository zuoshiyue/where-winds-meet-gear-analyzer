<template>
  <div class="analysis-panel">
    <!-- 流派选择 -->
    <div class="class-selector">
      <el-select v-model="selectedClass" placeholder="选择武器心法流派" style="width: 250px" @change="handleClassChange">
        <el-option-group
          v-for="group in flowGroups"
          :key="group.label"
          :label="group.label"
        >
          <el-option
            v-for="flow in group.flows"
            :key="flow.value"
            :label="flow.label"
            :value="flow.value"
          />
        </el-option-group>
      </el-select>
      <div class="class-description" v-if="getFlowDescription(selectedClass)">
        <el-tag type="info" size="small">{{ getFlowDescription(selectedClass) }}</el-tag>
      </div>
    </div>

    <!-- 装备列表 -->
    <el-table 
      :data="sortedEquipment" 
      style="width: 100%"
      @row-click="handleRowClick"
      highlight-current-row
    >
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column label="品质" width="100">
        <template #default="{ row }">
          <span v-for="i in row.quality" :key="i">⭐</span>
        </template>
      </el-table-column>
      <el-table-column label="等级" width="70">
        <template #default="{ row }">
          +{{ row.level }}
        </template>
      </el-table-column>
      <el-table-column prop="set_name" label="套装" width="120" />
      <el-table-column label="评分" width="100" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.scoreData.total_score)">
            {{ row.scoreData.total_score.toFixed(1) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="建议" min-width="200">
        <template #default="{ row }">
          <span class="recommendation">{{ row.scoreData.recommendation.substring(0, 30) }}...</span>
        </template>
      </el-table-column>
    </el-table>

    <!-- 评分详情 -->
    <div class="score-detail" v-if="selectedEquipment">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>评分详情 - {{ selectedEquipment.name }}</span>
          </div>
        </template>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="总评分">
            <el-tag size="large" :type="getScoreType(selectedEquipment.scoreData.total_score)">
              {{ selectedEquipment.scoreData.total_score.toFixed(1) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="职业">{{ selectedClass }}</el-descriptions-item>
          <el-descriptions-item label="品质分">{{ selectedEquipment.scoreData.quality_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="属性分">{{ selectedEquipment.scoreData.stats_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="强化分">{{ selectedEquipment.scoreData.level_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="套装加成">{{ selectedEquipment.scoreData.set_bonus.toFixed(1) }}</el-descriptions-item>
        </el-descriptions>

        <div class="recommendation-box">
          <h4>培养建议</h4>
          <p>{{ selectedEquipment.scoreData.recommendation }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { bulkScore, getFlowCategories } from '../utils/scorer'

const props = defineProps({
  equipmentList: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['view-detail'])

const selectedClass = ref('通用')
const selectedEquipment = ref(null)

// 流派分组
const flowGroups = computed(() => {
  const categories = getFlowCategories()
  return Object.entries(categories).map(([label, flows]) => ({
    label,
    flows: flows.map(flow => ({
      label: flow,
      value: flow,
    }))
  }))
})

// 批量评分
const scoredEquipment = computed(() => {
  return bulkScore(props.equipmentList, selectedClass.value)
})

// 按评分排序
const sortedEquipment = computed(() => {
  return [...scoredEquipment.value].sort(
    (a, b) => b.scoreData.total_score - a.scoreData.total_score
  )
})

// 处理流派切换
const handleClassChange = () => {
  selectedEquipment.value = null
}

// 处理行点击
const handleRowClick = (row) => {
  selectedEquipment.value = row
  emit('view-detail', row)
}

// 获取评分标签类型
const getScoreType = (score) => {
  if (score >= 200) return 'success'
  if (score >= 150) return 'warning'
  if (score >= 100) return ''
  return 'danger'
}

// 获取流派描述
const getFlowDescription = (flowName) => {
  const descriptions = {
    '通用': '通用配置，适合所有流派',
    '破竹·鸢': 'T0 极致爆发/无敌帧 - 剑 + 扇，竞速本必备',
    '牵丝·玉': 'T0 远程风筝/团队增益 - 弓 + 伞，单刷最安全',
    '破竹·风': 'T0.5 高频吸血/持续压制 - 剑 + 刀，站桩输出强',
    '破竹·尘': 'T0.5 强力控制/团队辅助 - 剑 + 笛，高难本必备',
    '鸣金·影': 'T0.5 流血爆发/近战缠斗 - 枪 + 剑，高爆发数字',
    '鸣金·虹': 'T1 中距离拉扯/新手友好 - 枪 + 弓，开荒体验极佳',
    '裂石·威': 'T1 绝对防御/反击输出 - 重剑 + 盾，生存率最高',
    '裂石·钧': 'T1 超级破韧/眩晕控制 - 重剑 + 锤，克制巨型 BOSS',
    '奇门·幻': 'T1 诡异身法/异常状态 - 扇 + 笛，PVP 强势',
    '游龙·水': 'T2 高机动/闪避反击 - 刀 + 扇，适合高手秀操作',
  }
  return descriptions[flowName] || ''
}
</script>

<style scoped>
.analysis-panel {
  padding: 20px;
}

.class-selector {
  margin-bottom: 20px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.class-description {
  min-width: 200px;
}

.recommendation {
  font-size: 13px;
  color: #666;
}

.score-detail {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recommendation-box {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.recommendation-box h4 {
  margin: 0 0 10px;
  color: #333;
}

.recommendation-box p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}
</style>
