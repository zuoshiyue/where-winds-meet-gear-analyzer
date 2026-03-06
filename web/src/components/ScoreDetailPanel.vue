<template>
  <div class="score-detail-panel">
    <el-dialog
      :model-value="visible"
      title="📊 评分详情"
      width="900px"
      @close="$emit('close')"
    >
      <!-- 装备基本信息 -->
      <el-card class="info-card" v-if="equipment">
        <template #header>
          <div class="card-header">
            <span class="equipment-name">{{ equipment.name }}</span>
            <el-tag :type="getQualityType(equipment.quality)" size="large">
              {{ getQualityText(equipment.quality) }}
            </el-tag>
          </div>
        </template>

        <el-descriptions :column="3" border>
          <el-descriptions-item label="装备类型">{{ equipment.type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="套装名称">{{ equipment.set_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="强化等级">+{{ equipment.level || 0 }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 评分总览 -->
      <el-card class="score-summary">
        <template #header>
          <div class="card-header">
            <span>🎯 评分总览 (职业：{{ scoreData.class_name }})</span>
            <el-tag :type="getScoreType(scoreData.total_score)" size="large">
              总分：{{ scoreData.total_score.toFixed(1) }}
            </el-tag>
          </div>
        </template>

        <el-row :gutter="20" class="score-bars">
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">品质分</span>
              <el-progress 
                :percentage="(scoreData.quality_score / 150) * 100" 
                :format="() => scoreData.quality_score.toFixed(1)"
                :status="scoreData.quality_score >= 100 ? 'success' : ''"
              />
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">属性分</span>
              <el-progress 
                :percentage="Math.min(100, (scoreData.stats_score / 200) * 100)" 
                :format="() => scoreData.stats_score.toFixed(1)"
                :status="scoreData.stats_score >= 150 ? 'success' : ''"
              />
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">强化分</span>
              <el-progress 
                :percentage="Math.min(100, (scoreData.level_score / 30) * 100)" 
                :format="() => scoreData.level_score.toFixed(1)"
              />
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">套装加成</span>
              <el-progress 
                :percentage="(scoreData.set_bonus / 20) * 100" 
                :format="() => scoreData.set_bonus.toFixed(1)"
                :status="scoreData.set_bonus >= 20 ? 'success' : ''"
              />
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 属性评分明细表 -->
      <el-card class="stats-table-card" v-if="equipment.stats && equipment.stats.length > 0">
        <template #header>
          <div class="card-header">
            <span>📈 属性评分明细</span>
            <el-tooltip content="展示每个属性的数值、权重和得分" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </div>
        </template>

        <el-table :data="statsWithScore" style="width: 100%" size="small" border>
          <el-table-column prop="name" label="属性名称" width="120" />
          <el-table-column prop="value" label="属性数值" width="120">
            <template #default="{ row }">
              {{ formatStatValue(row) }}
            </template>
          </el-table-column>
          <el-table-column prop="weight" label="职业权重" width="100">
            <template #default="{ row }">
              <el-tag size="small" :type="getWeightType(row.weight)">
                {{ row.weight.toFixed(1) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="单项得分" width="120">
            <template #default="{ row }">
              <span class="score-value">{{ (row.value * row.weight).toFixed(1) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="说明" />
        </el-table>

        <div class="formula-explanation">
          <h4>💡 计算公式</h4>
          <div class="formula">
            <code>属性分 = Σ(属性值 × 职业权重)</code>
          </div>
          <p class="note">
            不同职业对同一属性的权重不同。例如：输出职业暴击权重高，坦克职业防御权重高。
          </p>
        </div>
      </el-card>

      <!-- 评分标准参考表 -->
      <el-card class="reference-table-card">
        <template #header>
          <span>📋 评分标准参考</span>
        </template>

        <el-tabs>
          <el-tab-pane label="品质分">
            <el-table :data="qualityReference" size="small" border max-height="300">
              <el-table-column prop="quality" label="品质" width="100" />
              <el-table-column prop="stars" label="星级" width="100" />
              <el-table-column prop="score" label="基础分数" width="100" />
              <el-table-column prop="description" label="说明" />
            </el-table>
          </el-tab-pane>

          <el-tab-pane label="职业权重">
            <el-table :data="weightReference" size="small" border max-height="400">
              <el-table-column prop="stat" label="属性" width="100" />
              <el-table-column v-for="cls in activeClasses" :key="cls" :label="cls" width="100">
                <template #default="{ row }">
                  {{ row.weights[cls] ? row.weights[cls].toFixed(1) : '-' }}
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>

          <el-tab-pane label="评分等级">
            <el-table :data="scoreLevelReference" size="small" border>
              <el-table-column prop="level" label="等级" width="80" />
              <el-table-column prop="range" label="分数范围" width="150" />
              <el-table-column prop="description" label="评价" />
              <el-table-column prop="suggestion" label="建议" />
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <!-- 培养建议 -->
      <el-card class="recommendation-card" v-if="scoreData.recommendation">
        <template #header>
          <span>💬 培养建议</span>
        </template>
        <el-alert
          :title="scoreData.recommendation"
          :type="getRecommendationType(scoreData.total_score)"
          show-icon
          :closable="false"
        />
      </el-card>

      <template #footer>
        <el-button @click="$emit('close')">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { QuestionFilled } from '@element-plus/icons-vue'
import { calculateScore, CLASS_CONFIGS } from '../utils/scorer'

const props = defineProps({
  equipment: {
    type: Object,
    default: null
  },
  visible: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: '通用'
  }
})

const emit = defineEmits(['close'])

// 计算评分
const scoreData = computed(() => {
  if (!props.equipment) return {}
  return calculateScore(props.equipment, props.className)
})

// 带评分的属性列表
const statsWithScore = computed(() => {
  if (!props.equipment?.stats) return []
  
  const weights = CLASS_CONFIGS[props.className]?.stat_weights || {}
  
  return props.equipment.stats.map(stat => ({
    ...stat,
    weight: weights[stat.name] || 0.5,
    description: getStatDescription(stat.name, stat.value, weights[stat.name])
  }))
})

// 品质参考表
const qualityReference = computed(() => [
  { quality: '白色', stars: '⭐', score: 10, description: '普通品质，基础装备' },
  { quality: '绿色', stars: '⭐⭐', score: 30, description: '优秀品质，过渡使用' },
  { quality: '蓝色', stars: '⭐⭐⭐', score: 60, description: '稀有品质，值得培养' },
  { quality: '紫色', stars: '⭐⭐⭐⭐', score: 100, description: '史诗品质，重点培养' },
  { quality: '金色', stars: '⭐⭐⭐⭐⭐', score: 150, description: '传说品质，极品装备' },
])

// 职业权重参考表
const weightReference = computed(() => {
  const stats = ['attack', 'defense', 'health', 'crit', 'crit_damage', 'element_damage', 'speed']
  const statNames = {
    attack: '攻击',
    defense: '防御',
    health: '生命',
    crit: '暴击',
    crit_damage: '爆伤',
    element_damage: '元素伤害',
    speed: '速度',
  }
  
  return stats.map(stat => ({
    stat: statNames[stat],
    weights: Object.fromEntries(
      Object.entries(CLASS_CONFIGS).map(([cls, config]) => [
        cls,
        config.stat_weights[stat] || 0
      ])
    )
  }))
})

// 活跃职业列表
const activeClasses = ['通用', '剑客', '刀客', '枪客', '医仙', '拳师', '刺客']

// 评分等级参考表
const scoreLevelReference = [
  { level: 'S', range: '≥ 200', description: '极品装备', suggestion: '优先培养，作为毕业装备' },
  { level: 'A', range: '150-199', description: '优秀装备', suggestion: '值得培养，重点投入资源' },
  { level: 'B', range: '100-149', description: '普通装备', suggestion: '过渡使用，有更好就替换' },
  { level: 'C', range: '< 100', description: '较差装备', suggestion: '建议替换，可作为强化材料' },
]

// 获取属性说明
function getStatDescription(statName, value, weight) {
  const descriptions = {
    attack: '提高基础攻击力',
    defense: '提高物理防御力',
    health: '提高最大生命值',
    crit: '提高暴击概率',
    crit_damage: '提高暴击伤害倍率',
    element_damage: '提高元素技能伤害',
    speed: '提高攻击速度和移动速度',
  }
  
  const weightDesc = weight >= 1.8 ? '核心属性' : weight >= 1.3 ? '重要属性' : weight >= 1.0 ? '一般属性' : '次要属性'
  
  return `${descriptions[statName] || '未知属性'} - ${weightDesc}`
}

// 格式化属性值
function formatStatValue(row) {
  const percentStats = ['crit', 'crit_damage', 'element_damage', 'speed']
  const isPercent = percentStats.includes(row.name)
  return isPercent ? `${row.value}%` : row.value
}

// 获取品质类型
function getQualityType(quality) {
  const types = { 1: 'info', 2: 'success', 3: '', 4: 'warning', 5: 'danger' }
  return types[quality] || 'info'
}

// 获取品质文字
function getQualityText(quality) {
  const texts = { 1: '白色', 2: '绿色', 3: '蓝色', 4: '紫色', 5: '金色' }
  return texts[quality] || '未知'
}

// 获取评分类型
function getScoreType(score) {
  if (score >= 200) return 'success'
  if (score >= 150) return 'warning'
  if (score >= 100) return ''
  return 'danger'
}

// 获取权重类型
function getWeightType(weight) {
  if (weight >= 1.8) return 'danger'
  if (weight >= 1.5) return 'warning'
  if (weight >= 1.0) return ''
  return 'info'
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
.score-detail-panel {
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.equipment-name {
  font-size: 1.2em;
  font-weight: bold;
}

.info-card {
  margin-bottom: 20px;
}

.score-summary {
  margin-bottom: 20px;
}

.score-bars {
  margin-top: 15px;
}

.score-item {
  margin-bottom: 15px;
}

.score-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.score-value {
  font-weight: bold;
  color: #409EFF;
}

.stats-table-card {
  margin-bottom: 20px;
}

.formula-explanation {
  margin-top: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.formula-explanation h4 {
  margin: 0 0 10px;
  color: #303133;
}

.formula {
  background: white;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.formula code {
  font-family: 'Courier New', monospace;
  color: #e74c3c;
  font-size: 14px;
}

.note {
  margin: 0;
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
}

.reference-table-card {
  margin-bottom: 20px;
}

.recommendation-card {
  margin-bottom: 0;
}
</style>
