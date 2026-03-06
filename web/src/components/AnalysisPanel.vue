<template>
  <div class="analysis-panel">
    <!-- 职业选择 -->
    <div class="class-selector">
      <el-select v-model="selectedClass" placeholder="选择职业" style="width: 200px" @change="handleClassChange">
        <el-option label="通用" value="通用" />
        <el-option label="⚔️ 剑客" value="剑客" />
        <el-option label="🔪 刀客" value="刀客" />
        <el-option label="🛡️ 枪客" value="枪客" />
        <el-option label="💚 医仙" value="医仙" />
        <el-option label="👊 拳师" value="拳师" />
        <el-option label="🗡️ 刺客" value="刺客" />
      </el-select>
      <div class="class-description" v-if="getClassDescription(selectedClass)">
        <el-tag type="info" size="small">{{ getClassDescription(selectedClass) }}</el-tag>
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
import { bulkScore } from '../utils/scorer'

const props = defineProps({
  equipmentList: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['view-detail'])

const selectedClass = ref('通用')
const selectedEquipment = ref(null)

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

// 处理职业切换
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

// 获取职业描述
const getClassDescription = (className) => {
  const descriptions = {
    '通用': '通用配置，适合所有职业',
    '剑客': '近战输出，攻守兼备，高机动性',
    '刀客': '近战高攻击，快速击倒敌人',
    '枪客': '长柄武器，坦克型，扛伤输出兼具',
    '医仙': '辅助治疗，团队核心',
    '拳师': '近战格斗，高频率攻击',
    '刺客': '高风险高回报，一击必杀',
  }
  return descriptions[className] || ''
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
