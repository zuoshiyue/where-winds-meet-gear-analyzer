<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="app-header">
      <div class="logo-section">
        <img src="/logo.svg" alt="燕云十六声" class="game-logo" onerror="this.style.display='none'" />
        <div class="title-section">
          <h1>🎮 燕云装备助手</h1>
          <p class="subtitle">燕云十六声装备分析工具</p>
        </div>
      </div>
      
      <!-- 下载工具按钮 -->
      <div class="download-tool">
        <el-button
          type="warning"
          size="large"
          @click="openDownloadPage"
          class="download-btn"
        >
          <el-icon><Download /></el-icon>
          下载自动截图工具
        </el-button>
        <p class="tool-tip">一键下载 PC 端自动截图脚本 · 热键 F9 快速捕获</p>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 截图上传 -->
        <el-tab-pane label="📸 截图上传" name="upload">
          <ImageUploader @upload-complete="handleUploadComplete" />
        </el-tab-pane>

        <!-- 装备列表 -->
        <el-tab-pane label="📋 装备列表" name="equipment">
          <EquipmentList 
            :equipment-list="equipmentList"
            @view-detail="handleViewDetail"
            @delete="handleDelete"
          />
        </el-tab-pane>

        <!-- 装备分析 -->
        <el-tab-pane label="📊 装备分析" name="analysis">
          <AnalysisPanel 
            :equipment-list="equipmentList"
            @view-detail="handleViewDetail"
          />
        </el-tab-pane>

        <!-- 数据统计 -->
        <el-tab-pane label="📈 数据统计" name="stats">
          <StatsChart :equipment-list="equipmentList" />
        </el-tab-pane>

        <!-- 设置 -->
        <el-tab-pane label="⚙️ 设置" name="settings">
          <SettingsPanel />
        </el-tab-pane>
      </el-tabs>
    </main>

    <!-- 装备详情弹窗 -->
    <EquipmentDetail 
      v-if="selectedEquipment"
      :equipment="selectedEquipment"
      :visible="showDetail"
      @close="showDetail = false"
      @view-detail="handleViewScoreDetail"
    />

    <!-- 评分详情面板 -->
    <ScoreDetailPanel
      v-if="selectedEquipment"
      :equipment="selectedEquipment"
      :visible="showScoreDetail"
      :class-name="selectedClass"
      @close="showScoreDetail = false"
    />

    <!-- 底部 -->
    <footer class="app-footer">
      <p>
        <span>v0.1.0</span>
        <span class="divider">|</span>
        <span>纯前端应用 · 数据本地存储</span>
        <span class="divider">|</span>
        <a href="https://github.com/zuoshiyue/where-winds-meet-gear-analyzer" target="_blank">GitHub</a>
      </p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import ImageUploader from './components/ImageUploader.vue'
import EquipmentList from './components/EquipmentList.vue'
import AnalysisPanel from './components/AnalysisPanel.vue'
import StatsChart from './components/StatsChart.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import EquipmentDetail from './components/EquipmentDetail.vue'
import ScoreDetailPanel from './components/ScoreDetailPanel.vue'
import { useEquipment } from './composables/useEquipment'

const activeTab = ref('upload')
const showDetail = ref(false)
const showScoreDetail = ref(false)
const selectedEquipment = ref(null)
const selectedClass = ref('通用')

const { equipmentList, loadEquipment, addEquipment, deleteEquipment } = useEquipment()

// 加载装备数据
onMounted(async () => {
  await loadEquipment()
})

// 处理上传完成
const handleUploadComplete = async (equipments) => {
  for (const eq of equipments) {
    await addEquipment(eq)
  }
  ElMessage.success(`成功添加 ${equipments.length} 个装备`)
  activeTab.value = 'equipment'
}

// 查看详情
const handleViewDetail = (equipment) => {
  selectedEquipment.value = equipment
  showDetail.value = true
}

// 查看详细评分
const handleViewScoreDetail = (equipment) => {
  selectedEquipment.value = equipment
  showScoreDetail.value = true
}

// 删除装备
const handleDelete = async (id) => {
  await deleteEquipment(id)
  ElMessage.success('删除成功')
}

// 打开下载页面
const openDownloadPage = () => {
  // 直接下载工具包
  const downloadUrl = '/tools/燕云装备助手.zip'
  
  const a = document.createElement('a')
  a.href = downloadUrl
  a.download = '燕云装备助手 - 工具包.zip'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  
  ElMessage.success('📦 下载已开始，请查看浏览器下载栏')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.app-header {
  text-align: center;
  color: white;
  margin-bottom: 20px;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 10px;
}

.game-logo {
  height: 60px;
  width: auto;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
}

.title-section {
  text-align: left;
}

.app-header h1 {
  margin: 0;
  font-size: 2em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  margin: 10px 0 0;
  font-size: 1.1em;
  opacity: 0.9;
}

.download-tool {
  margin-top: 20px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  display: inline-block;
}

.download-btn {
  height: 50px;
  font-size: 16px;
  font-weight: bold;
  padding: 0 30px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.4);
  transition: all 0.3s;
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.6);
}

.tool-tip {
  margin: 10px 0 0;
  font-size: 0.9em;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
}

.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

:deep(.el-tabs--border-card) {
  background: white;
  border: none;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.app-footer {
  text-align: center;
  color: white;
  margin-top: 20px;
  padding: 10px;
  opacity: 0.8;
}

.app-footer a {
  color: white;
  text-decoration: underline;
}

.divider {
  margin: 0 10px;
}
</style>
