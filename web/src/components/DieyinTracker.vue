<template>
  <div class="dieyin-tracker">
    <el-card class="tracker-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="title">🎯 叠音追踪</span>
          <el-button size="small" @click="resetTracker">重置</el-button>
        </div>
      </template>

      <div class="tracker-content">
        <!-- 当前状态 -->
        <div class="current-status">
          <div class="status-title">📊 当前状态</div>
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item label="叠音等级">
              {{ currentLevel }} / {{ maxLevel }}
            </el-descriptions-item>
            <el-descriptions-item label="词条数量">
              {{ currentStats.length }} / 4
            </el-descriptions-item>
            <el-descriptions-item label="当前评分">
              <span :class="['score', getScoreClass(currentScore)]">
                {{ currentScore }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="装备评级">
              <el-tag :type="getGradeType(currentGrade)" size="small">
                {{ currentGrade }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 词条列表 -->
        <div class="stats-list">
          <div class="list-title">📝 词条详情</div>
          <el-table :data="currentStats" size="small" stripe>
            <el-table-column prop="statName" label="词条名称" />
            <el-table-column prop="statValue" label="数值" width="80" />
            <el-table-column prop="weight" label="权重" width="80">
              <template #default="{ row }">
                <span :class="['weight', getWeightClass(row.weight)]">
                  {{ row.weight.toFixed(2) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="得分" width="80" />
            <el-table-column label="类型" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.isCore" type="warning" size="small">核心</el-tag>
                <el-tag v-else-if="row.isValid" type="success" size="small">有效</el-tag>
                <el-tag v-else type="info" size="small">一般</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 叠音历史 -->
        <div class="dieyin-history">
          <div class="history-title">📈 叠音历史</div>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in history"
              :key="index"
              :timestamp="record.timestamp"
              placement="top"
              :color="getTimelineColor(record.change)"
            >
              <el-card shadow="hover">
                <div class="history-item">
                  <div class="history-header">
                    <span class="level-tag">叠音 +{{ index + 1 }}</span>
                    <span :class="['change', record.change > 0 ? 'positive' : 'negative']">
                      {{ record.change > 0 ? '+' : '' }}{{ record.change }} ({{ record.changePercent }}%)
                    </span>
                  </div>
                  <div class="history-score">
                    评分：{{ record.beforeScore }} → {{ record.afterScore }}
                  </div>
                  <div class="history-advice">
                    {{ record.advice }}
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>

        <!-- 操作按钮 -->
        <div class="actions">
          <el-button
            type="primary"
            @click="addDieyinRecord"
            :disabled="currentLevel >= maxLevel"
            block
          >
            ✨ 记录下一次叠音
          </el-button>
          
          <el-button
            type="success"
            @click="exportReport"
            :disabled="history.length === 0"
            block
          >
            📊 导出培养报告
          </el-button>
        </div>

        <!-- 继续培养建议 -->
        <div class="continue-advice">
          <el-alert
            :title="continueAdvice.reason"
            :type="continueAdvice.continue ? 'info' : 'warning'"
            :closable="false"
            show-icon
          >
            <template #title>
              <div class="advice-content">
                <span>{{ continueAdvice.reason }}</span>
                <el-tag v-if="continueAdvice.continue" type="success" size="small">继续</el-tag>
                <el-tag v-else type="warning" size="small">止损</el-tag>
              </div>
            </template>
          </el-alert>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { calculateDieyinScore, compareDieyin, shouldContinueDieyin } from '../utils/embryo.js'

const props = defineProps({
  embryoData: {
    type: Object,
    default: null,
  },
  flow: {
    type: String,
    default: '通用',
  },
})

const maxLevel = 5
const currentLevel = ref(0)
const history = ref([])
const currentStats = ref([])

// 初始化
watch(() => props.embryoData, (newData) => {
  if (newData) {
    currentStats.value = [{
      statName: newData.statName,
      statValue: newData.statValue,
    }]
    currentLevel.value = 0
    history.value = []
  }
}, { immediate: true })

// 当前评分
const currentScore = computed(() => {
  const result = calculateDieyinScore(currentStats.value, props.flow)
  return result.totalScore
})

// 当前评级
const currentGrade = computed(() => {
  const result = calculateDieyinScore(currentStats.value, props.flow)
  return result.grade
})

// 继续培养建议
const continueAdvice = computed(() => {
  const current = calculateDieyinScore(currentStats.value, props.flow)
  return shouldContinueDieyin(current, currentLevel.value, props.flow)
})

// 添加叠音记录
const addDieyinRecord = () => {
  // TODO: 打开对话框让用户输入新的词条
  console.log('添加叠音记录')
}

// 重置追踪器
const resetTracker = () => {
  currentLevel.value = 0
  history.value = []
  if (props.embryoData) {
    currentStats.value = [{
      statName: props.embryoData.statName,
      statValue: props.embryoData.statValue,
    }]
  }
}

// 获取评分样式
const getScoreClass = (score) => {
  if (score >= 100) return 'score-excellent'
  if (score >= 60) return 'score-good'
  return 'score-normal'
}

// 获取权重样式
const getWeightClass = (weight) => {
  if (weight >= 1.3) return 'weight-core'
  if (weight >= 0.8) return 'weight-valid'
  return 'weight-normal'
}

// 获取评级类型
const getGradeType = (grade) => {
  if (grade === '毕业候选') return 'success'
  if (grade === '优质散件') return 'primary'
  return 'info'
}

// 获取时间轴颜色
const getTimelineColor = (change) => {
  if (change > 0) return '#67C23A'
  return '#F56C6C'
}

// 导出报告
const exportReport = () => {
  console.log('导出培养报告')
}
</script>

<style scoped lang="scss">
.dieyin-tracker {
  width: 100%;
}

.tracker-card {
  :deep(.el-card__header) {
    padding: 12px 16px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-bottom: none;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .title {
    font-size: 16px;
    font-weight: bold;
    color: white;
  }
}

.tracker-content {
  .current-status {
    margin-bottom: 20px;

    .status-title {
      font-size: 14px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 12px;
    }

    .score {
      font-weight: bold;
      font-size: 16px;
      
      &.score-excellent { color: #67C23A; }
      &.score-good { color: #409EFF; }
      &.score-normal { color: #909399; }
    }
  }

  .stats-list {
    margin-bottom: 20px;

    .list-title {
      font-size: 14px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 12px;
    }

    .weight {
      font-weight: 500;
      
      &.weight-core { color: #E6A23C; }
      &.weight-valid { color: #67C23A; }
      &.weight-normal { color: #909399; }
    }
  }

  .dieyin-history {
    margin-bottom: 20px;

    .history-title {
      font-size: 14px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 12px;
    }

    .history-item {
      .history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;

        .level-tag {
          font-weight: bold;
          color: #409EFF;
        }

        .change {
          font-weight: bold;
          
          &.positive { color: #67C23A; }
          &.negative { color: #F56C6C; }
        }
      }

      .history-score {
        font-size: 13px;
        color: #606266;
        margin-bottom: 4px;
      }

      .history-advice {
        font-size: 12px;
        color: #909399;
        font-style: italic;
      }
    }
  }

  .actions {
    margin-bottom: 20px;

    .el-button {
      margin-bottom: 12px;
    }
  }

  .continue-advice {
    .advice-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>
