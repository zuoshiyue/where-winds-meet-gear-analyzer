<template>
  <div class="embryo-evaluator">
    <el-card class="evaluator-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="title">🌱 胚子评估</span>
          <el-tag :type="result.worthCultivating ? 'success' : 'info'" size="small">
            {{ result.worthCultivating ? '值得培养' : '不建议培养' }}
          </el-tag>
        </div>
      </template>

      <div v-if="embryoData" class="evaluator-content">
        <!-- 胚子信息 -->
        <div class="embryo-info">
          <div class="info-row">
            <span class="label">装备类型：</span>
            <span class="value">{{ embryoData.equipmentType || '未知' }}</span>
          </div>
          <div class="info-row">
            <span class="label">当前流派：</span>
            <span class="value">{{ embryoData.flow || '通用' }}</span>
          </div>
          <div class="info-row">
            <span class="label">基础词条：</span>
            <span class="value stat-highlight">
              {{ embryoData.statName }} +{{ embryoData.statValue }}
            </span>
          </div>
        </div>

        <!-- 评估结果 -->
        <div class="evaluation-result">
          <div class="rating-display" :style="{ color: result.color }">
            <span class="rating-grade">{{ result.rating }}</span>
            <span class="rating-label">{{ result.label }}</span>
          </div>
          
          <div class="score-display">
            <el-progress
              :percentage="Math.min(100, (result.embryoScore / result.expectedFinalScore) * 100)"
              :color="result.color"
              :format="() => `胚子评分：${result.embryoScore} / 期望${result.expectedFinalScore}`"
            />
          </div>
        </div>

        <!-- 权重分析 -->
        <div class="weight-analysis">
          <div class="analysis-title">📊 权重分析</div>
          <el-descriptions :column="1" size="small">
            <el-descriptions-item label="词条权重">
              {{ result.weight.toFixed(2) }}
            </el-descriptions-item>
            <el-descriptions-item label="流派适配">
              {{ getFlowAdaptation(result.weight) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 培养建议 -->
        <div class="cultivation-advice">
          <div class="advice-title">💡 培养建议</div>
          <el-alert
            :title="result.advice"
            :type="result.worthCultivating ? 'success' : 'warning'"
            show-icon
            :closable="false"
          />
        </div>

        <!-- 详细分析 -->
        <div class="detailed-analysis">
          <el-divider content-position="left">📝 详细分析</el-divider>
          <p class="analysis-text">{{ result.analysis }}</p>
        </div>

        <!-- 叠音追踪入口 -->
        <div class="dieyin-tracker-entry">
          <el-button
            type="primary"
            :disabled="!result.worthCultivating"
            @click="$emit('start-tracking', embryoData)"
            block
          >
            🎯 开始叠音追踪
          </el-button>
          <p v-if="!result.worthCultivating" class="hint">
            胚子评级较低，不建议投入资源叠音
          </p>
        </div>
      </div>

      <div v-else class="empty-state">
        <el-empty description="请先上传或识别装备胚子" :image-size="80" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { evaluateEmbryo } from '../utils/embryo.js'

const props = defineProps({
  embryoData: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['start-tracking'])

// 评估结果
const result = computed(() => {
  if (!props.embryoData) {
    return {
      rating: '-',
      label: '等待评估',
      advice: '',
      color: '#909399',
      embryoScore: 0,
      weight: 0,
      worthCultivating: false,
      expectedFinalScore: 0,
      analysis: '',
    }
  }
  return evaluateEmbryo(props.embryoData)
})

// 获取流派适配描述
const getFlowAdaptation = (weight) => {
  if (weight >= 1.3) return '完美适配 ⭐⭐⭐⭐⭐'
  if (weight >= 1.1) return '高度适配 ⭐⭐⭐⭐'
  if (weight >= 0.9) return '基本适配 ⭐⭐⭐'
  return '适配度低 ⭐⭐'
}
</script>

<style scoped lang="scss">
.embryo-evaluator {
  width: 100%;
}

.evaluator-card {
  :deep(.el-card__header) {
    padding: 12px 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.evaluator-content {
  .embryo-info {
    margin-bottom: 20px;
    padding: 12px;
    background: #f5f7fa;
    border-radius: 8px;

    .info-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      
      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: #606266;
        font-size: 14px;
      }

      .value {
        color: #303133;
        font-weight: 500;
      }

      .stat-highlight {
        color: #409EFF;
        font-weight: bold;
        font-size: 15px;
      }
    }
  }

  .evaluation-result {
    margin-bottom: 20px;
    text-align: center;

    .rating-display {
      margin-bottom: 16px;

      .rating-grade {
        font-size: 48px;
        font-weight: bold;
        display: block;
      }

      .rating-label {
        font-size: 14px;
        color: #606266;
      }
    }

    .score-display {
      margin-top: 12px;
    }
  }

  .weight-analysis {
    margin-bottom: 20px;
    padding: 12px;
    background: #f5f7fa;
    border-radius: 8px;

    .analysis-title {
      font-size: 14px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 12px;
    }
  }

  .cultivation-advice {
    margin-bottom: 20px;

    .advice-title {
      font-size: 14px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 12px;
    }
  }

  .detailed-analysis {
    margin-bottom: 20px;

    .analysis-text {
      font-size: 14px;
      color: #606266;
      line-height: 1.6;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 8px;
    }
  }

  .dieyin-tracker-entry {
    .hint {
      margin-top: 8px;
      font-size: 12px;
      color: #909399;
      text-align: center;
    }
  }
}

.empty-state {
  padding: 40px 0;
}
</style>
