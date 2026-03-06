<template>
  <div class="equipment-detail">
    <el-dialog
      :model-value="visible"
      title="装备详情"
      width="600px"
      @close="$emit('close')"
    >
      <!-- 装备基本信息 -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="名称">{{ equipment.name }}</el-descriptions-item>
        <el-descriptions-item label="品质">
          <span v-for="i in equipment.quality" :key="i">⭐</span>
        </el-descriptions-item>
        <el-descriptions-item label="类型">{{ equipment.type || '未分类' }}</el-descriptions-item>
        <el-descriptions-item label="等级">+{{ equipment.level }}</el-descriptions-item>
        <el-descriptions-item label="套装">{{ equipment.set_name || '无' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(equipment.created_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 属性列表 -->
      <div class="stats-section" v-if="equipment.stats && equipment.stats.length > 0">
        <h4>属性</h4>
        <el-table :data="equipment.stats" size="small">
          <el-table-column prop="name" label="属性名" />
          <el-table-column prop="value" label="数值" />
        </el-table>
      </div>

      <!-- 评分信息 -->
      <div class="score-section">
        <h4>评分信息</h4>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="总评分">
            <el-tag size="large" :type="getScoreType(scoreData.total_score)">
              {{ scoreData.total_score.toFixed(1) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="职业">{{ scoreData.class_name }}</el-descriptions-item>
          <el-descriptions-item label="品质分">{{ scoreData.quality_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="属性分">{{ scoreData.stats_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="强化分">{{ scoreData.level_score.toFixed(1) }}</el-descriptions-item>
          <el-descriptions-item label="套装加成">{{ scoreData.set_bonus.toFixed(1) }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="view-detail-btn">
          <el-button type="primary" @click="$emit('view-detail', equipment)">
            📊 查看详细评分计算过程
          </el-button>
        </div>
      </div>

      <!-- 培养建议 -->
      <div class="recommendation-section">
        <h4>培养建议</h4>
        <el-alert
          :title="scoreData.recommendation"
          :type="getRecommendationType(scoreData.total_score)"
          show-icon
          :closable="false"
        />
      </div>

      <!-- 截图预览 -->
      <div class="screenshot-section" v-if="equipment.screenshot_path">
        <h4>截图</h4>
        <el-image
          :src="equipment.screenshot_path"
          fit="contain"
          style="max-width: 100%; max-height: 300px"
        />
      </div>

      <template #footer>
        <el-button @click="$emit('close')">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { calculateScore } from '../utils/scorer'

const props = defineProps({
  equipment: {
    type: Object,
    required: true
  },
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// 计算评分
const scoreData = computed(() => {
  return calculateScore(props.equipment)
})

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 获取评分标签类型
function getScoreType(score) {
  if (score >= 200) return 'success'
  if (score >= 150) return 'warning'
  if (score >= 100) return ''
  return 'danger'
}

// 获取建议类型
function getRecommendationType(score) {
  if (score >= 200) return 'success'
  if (score >= 150) return 'warning'
  if (score >= 100) return 'info'
  return 'error'
}
</script>

<style scoped>
.equipment-detail {
}

.stats-section,
.score-section,
.recommendation-section,
.screenshot-section {
  margin-top: 20px;
}

h4 {
  margin: 0 0 10px;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.view-detail-btn {
  margin-top: 15px;
  text-align: center;
}
</style>
