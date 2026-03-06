<template>
  <div class="stats-chart">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">装备总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.avg_level }}</div>
            <div class="stat-label">平均等级</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ highScoreCount }}</div>
            <div class="stat-label">高分装备</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ goldenCount }}</div>
            <div class="stat-label">金色装备</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row :gutter="20" class="charts">
      <el-col :span="12">
        <el-card>
          <template #header>品质分布</template>
          <div ref="qualityChartRef" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>类型分布</template>
          <div ref="typeChartRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { calculateScore } from '../utils/scorer'

const props = defineProps({
  equipmentList: {
    type: Array,
    default: () => []
  }
})

const qualityChartRef = ref(null)
const typeChartRef = ref(null)

let qualityChart = null
let typeChart = null

// 统计数据
const stats = computed(() => {
  const total = props.equipmentList.length
  const avgLevel = total > 0 
    ? (props.equipmentList.reduce((sum, eq) => sum + (eq.level || 0), 0) / total).toFixed(1)
    : 0

  return {
    total,
    avg_level: avgLevel,
  }
})

// 高分装备数量
const highScoreCount = computed(() => {
  return props.equipmentList.filter(eq => {
    const score = calculateScore(eq).total_score
    return score >= 150
  }).length
})

// 金色装备数量
const goldenCount = computed(() => {
  return props.equipmentList.filter(eq => eq.quality === 5).length
})

// 品质分布数据
const qualityData = computed(() => {
  const data = [0, 0, 0, 0, 0]
  props.equipmentList.forEach(eq => {
    if (eq.quality >= 1 && eq.quality <= 5) {
      data[eq.quality - 1]++
    }
  })
  return data
})

// 类型分布数据
const typeData = computed(() => {
  const data = {}
  props.equipmentList.forEach(eq => {
    const type = eq.type || '未知'
    data[type] = (data[type] || 0) + 1
  })
  return Object.entries(data).map(([name, value]) => ({ name, value }))
})

// 初始化图表
onMounted(() => {
  if (qualityChartRef.value) {
    qualityChart = echarts.init(qualityChartRef.value)
  }
  if (typeChartRef.value) {
    typeChart = echarts.init(typeChartRef.value)
  }
  
  updateCharts()
})

// 监听数据变化
watch(() => props.equipmentList, () => {
  updateCharts()
}, { deep: true })

// 更新图表
function updateCharts() {
  if (!qualityChart || !typeChart) return

  // 品质分布图
  qualityChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['白色', '绿色', '蓝色', '紫色', '金色']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: qualityData.value,
      type: 'bar',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#83bff6' },
          { offset: 1, color: '#188df0' }
        ])
      }
    }]
  })

  // 类型分布图
  typeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      type: 'pie',
      radius: '50%',
      data: typeData.value,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  })
}

// 窗口大小变化时重新渲染
window.addEventListener('resize', () => {
  qualityChart?.resize()
  typeChart?.resize()
})
</script>

<style scoped>
.stats-chart {
  padding: 20px;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 10px;
}

.stat-value {
  font-size: 2.5em;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  color: #666;
}

.chart {
  height: 300px;
  width: 100%;
}
</style>
