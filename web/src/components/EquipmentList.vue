<template>
  <div class="equipment-list">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-input
        v-model="searchText"
        placeholder="搜索装备名称..."
        clearable
        style="width: 200px"
        @input="filterEquipment"
      >
        <template #prefix>
          <el-icon><search /></el-icon>
        </template>
      </el-input>

      <el-select v-model="filters.quality" placeholder="品质" clearable style="width: 120px" @change="filterEquipment">
        <el-option label="白色" :value="1" />
        <el-option label="绿色" :value="2" />
        <el-option label="蓝色" :value="3" />
        <el-option label="紫色" :value="4" />
        <el-option label="金色" :value="5" />
      </el-select>

      <el-select v-model="filters.type" placeholder="类型" clearable style="width: 100px" @change="filterEquipment">
        <el-option label="武器" value="武器" />
        <el-option label="防具" value="防具" />
        <el-option label="饰品" value="饰品" />
      </el-select>

      <el-select v-model="sortBy" placeholder="排序" style="width: 120px" @change="sortEquipment">
        <el-option label="评分" value="score" />
        <el-option label="品质" value="quality" />
        <el-option label="等级" value="level" />
        <el-option label="名称" value="name" />
      </el-select>

      <el-button type="primary" @click="exportCSV">导出 CSV</el-button>
    </div>

    <!-- 装备表格 -->
    <el-table 
      :data="filteredList" 
      style="width: 100%"
      @row-dblclick="handleRowDoubleClick"
      empty-text="暂无装备数据，请上传截图"
    >
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="type" label="类型" width="80" />
      <el-table-column label="品质" width="100">
        <template #default="{ row }">
          <span v-for="i in row.quality" :key="i" class="star">⭐</span>
        </template>
      </el-table-column>
      <el-table-column label="等级" width="80">
        <template #default="{ row }">
          +{{ row.level }}
        </template>
      </el-table-column>
      <el-table-column prop="set_name" label="套装" width="120" />
      <el-table-column label="评分" width="100" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.score)">
            {{ row.score?.toFixed(1) || '0.0' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleView(row)">详情</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination" v-if="filteredList.length > 10">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredList.length"
        layout="total, prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { calculateScore } from '../utils/scorer'

const props = defineProps({
  equipmentList: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['view-detail', 'delete'])

const searchText = ref('')
const filters = ref({
  quality: null,
  type: null
})
const sortBy = ref('score')
const currentPage = ref(1)
const pageSize = 20

// 计算装备评分
const equipmentWithScore = computed(() => {
  return props.equipmentList.map(eq => ({
    ...eq,
    score: calculateScore(eq).total_score
  }))
})

// 筛选后的列表
const filteredList = computed(() => {
  let result = [...equipmentWithScore.value]

  // 搜索过滤
  if (searchText.value) {
    result = result.filter(eq => 
      eq.name.toLowerCase().includes(searchText.value.toLowerCase())
    )
  }

  // 品质过滤
  if (filters.value.quality) {
    result = result.filter(eq => eq.quality === filters.value.quality)
  }

  // 类型过滤
  if (filters.value.type) {
    result = result.filter(eq => eq.type === filters.value.type)
  }

  // 排序
  if (sortBy.value === 'score') {
    result.sort((a, b) => (b.score || 0) - (a.score || 0))
  } else if (sortBy.value === 'quality') {
    result.sort((a, b) => b.quality - a.quality)
  } else if (sortBy.value === 'level') {
    result.sort((a, b) => b.level - a.level)
  } else if (sortBy.value === 'name') {
    result.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'))
  }

  return result
})

// 筛选装备
const filterEquipment = () => {
  currentPage.value = 1
}

// 排序装备
const sortEquipment = () => {
  // 由 computed 属性自动处理
}

// 获取评分标签类型
const getScoreType = (score) => {
  if (!score) return 'info'
  if (score >= 200) return 'success'
  if (score >= 150) return 'warning'
  if (score >= 100) return ''
  return 'danger'
}

// 查看详情
const handleView = (row) => {
  emit('view-detail', row)
}

// 删除装备
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除 "${row.name}" 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    emit('delete', row.id)
  }).catch(() => {})
}

// 双击查看详情
const handleRowDoubleClick = (row) => {
  handleView(row)
}

// 导出 CSV
const exportCSV = () => {
  const headers = ['ID', '名称', '类型', '品质', '等级', '套装', '评分']
  const rows = filteredList.value.map(eq => [
    eq.id,
    eq.name,
    eq.type,
    eq.quality,
    eq.level,
    eq.set_name || '',
    (eq.score || 0).toFixed(1)
  ])

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')

  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `装备列表_${new Date().toISOString().split('T')[0]}.csv`
  link.click()
  
  ElMessage.success('导出成功')
}
</script>

<style scoped>
.equipment-list {
  padding: 20px;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.star {
  font-size: 14px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
