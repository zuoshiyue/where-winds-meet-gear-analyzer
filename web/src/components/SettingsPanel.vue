<template>
  <div class="settings-panel">
    <el-form label-width="120px">
      <!-- OCR 设置 -->
      <el-form-item label="OCR 语言">
        <el-select v-model="ocrLang" placeholder="选择语言">
          <el-option label="简体中文" value="chi_sim" />
          <el-option label="英文" value="eng" />
          <el-option label="混合" value="chi_sim+eng" />
        </el-select>
      </el-form-item>

      <el-form-item label="使用 GPU">
        <el-switch v-model="useGPU" />
        <span class="tip">需要浏览器支持 WebGPU</span>
      </el-form-item>

      <el-form-item label="置信度阈值">
        <el-slider v-model="confidenceThreshold" :min="0" :max="1" :step="0.1" />
      </el-form-item>

      <!-- 数据管理 -->
      <el-form-item label="导出数据">
        <el-button type="primary" @click="handleExport">导出 JSON</el-button>
        <el-button @click="handleExportCSV">导出 CSV</el-button>
      </el-form-item>

      <el-form-item label="导入数据">
        <input
          type="file"
          ref="fileInput"
          accept=".json"
          style="display: none"
          @change="handleImport"
        />
        <el-button type="primary" @click="$refs.fileInput.click()">导入 JSON</el-button>
        <span class="tip">导入会追加数据，不会清空现有数据</span>
      </el-form-item>

      <el-form-item label="清空数据">
        <el-button type="danger" @click="handleClear">清空所有装备</el-button>
        <span class="tip">此操作不可恢复，请谨慎操作</span>
      </el-form-item>

      <!-- 流派配置 -->
      <el-divider />

      <el-form-item label="流派配置">
        <div class="class-configs">
          <el-collapse>
            <el-collapse-item title="⚔️ 九剑·输出" name="1">
              <div class="config-item">
                <p><strong>定位：</strong>九剑输出，攻守兼备，高机动性</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 ≈ 爆伤 > 速度</p>
                <p><strong>推荐套装：</strong>剑心套装、疾风套装、暴击套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🔪 唐横刀·狂战" name="2">
              <div class="config-item">
                <p><strong>定位：</strong>唐横刀狂战，极致输出，快速击倒</p>
                <p><strong>核心属性：</strong>攻击 > 爆伤 > 暴击</p>
                <p><strong>推荐套装：</strong>霸刀套装、铁血套装、强攻套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🗡️ 双刀·刺客" name="3">
              <div class="config-item">
                <p><strong>定位：</strong>双刀刺客，高风险高回报，一击必杀</p>
                <p><strong>核心属性：</strong>暴击 ≈ 爆伤 > 速度 > 攻击</p>
                <p><strong>推荐套装：</strong>暗影套装、潜行套装、暴击套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🛡️ 九枪·坦克" name="4">
              <div class="config-item">
                <p><strong>定位：</strong>九枪坦克，扛伤输出兼具</p>
                <p><strong>核心属性：</strong>防御 ≈ 生命 > 攻击</p>
                <p><strong>推荐套装：</strong>防御套装、坦克套装、生命套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🛡️ 裂石钧·防御" name="5">
              <div class="config-item">
                <p><strong>定位：</strong>裂石钧防御，以守为攻，反弹伤害</p>
                <p><strong>核心属性：</strong>防御 > 生命 > 攻击</p>
                <p><strong>推荐套装：</strong>玄钧套装、防御套装、反震套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="💚 医仙·治疗" name="6">
              <div class="config-item">
                <p><strong>定位：</strong>医仙治疗，团队核心，救死扶伤</p>
                <p><strong>核心属性：</strong>生命 > 防御 > 暴击</p>
                <p><strong>推荐套装：</strong>治疗套装、辅助套装、生命套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🎵 伞扇·辅助" name="7">
              <div class="config-item">
                <p><strong>定位：</strong>伞扇辅助，控制增益，团队支援</p>
                <p><strong>核心属性：</strong>生命 > 元素 > 防御</p>
                <p><strong>推荐套装：</strong>音律套装、辅助套装、控制套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="👊 无名·基础" name="8">
              <div class="config-item">
                <p><strong>定位：</strong>无名基础，平衡发展，新手推荐</p>
                <p><strong>核心属性：</strong>全属性平衡</p>
                <p><strong>推荐套装：</strong>无名套装、通用套装</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="🔮 嗟夫·特殊" name="9">
              <div class="config-item">
                <p><strong>定位：</strong>嗟夫特殊，独特机制，灵活多变</p>
                <p><strong>核心属性：</strong>暴击 > 爆伤 > 元素</p>
                <p><strong>推荐套装：</strong>嗟夫套装、特殊套装</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-form-item>

      <!-- 关于 -->
      <el-divider />

      <el-form-item label="应用版本">
        <span>v0.1.0</span>
      </el-form-item>

      <el-form-item label="GitHub">
        <el-link
          type="primary"
          href="https://github.com/zuoshiyue/where-winds-meet-gear-analyzer"
          target="_blank"
        >
          查看源码
        </el-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as storage from '../utils/storage'

const ocrLang = ref('chi_sim')
const useGPU = ref(false)
const confidenceThreshold = ref(0.6)

// 导出 JSON
async function handleExport() {
  try {
    const data = await storage.exportData()
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `装备数据_${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(`导出失败：${error.message}`)
  }
}

// 导出 CSV
async function handleExportCSV() {
  try {
    const equipments = await storage.getAllEquipment()
    const headers = ['ID', '名称', '类型', '品质', '等级', '套装', '创建时间']
    const rows = equipments.map(eq => [
      eq.id,
      eq.name,
      eq.type || '',
      eq.quality,
      eq.level,
      eq.set_name || '',
      eq.created_at || ''
    ])

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n')

    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `装备列表_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(`导出失败：${error.message}`)
  }
}

// 导入 JSON
async function handleImport(event) {
  const file = event.target.files[0]
  if (!file) return

  try {
    const text = await file.text()
    await storage.importData(text)
    ElMessage.success('导入成功，请刷新页面')
    event.target.value = ''
  } catch (error) {
    ElMessage.error(`导入失败：${error.message}`)
  }
}

// 清空所有数据
async function handleClear() {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有装备数据吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await storage.clearAllEquipment()
    ElMessage.success('清空成功，请刷新页面')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`清空失败：${error.message}`)
    }
  }
}
</script>

<style scoped>
.settings-panel {
  padding: 20px;
  max-width: 600px;
}

.tip {
  margin-left: 10px;
  font-size: 12px;
  color: #999;
}

.class-configs {
  width: 100%;
}

.config-item {
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.config-item p {
  margin: 5px 0;
  font-size: 13px;
  color: #606266;
}

.config-item strong {
  color: #303133;
}
</style>
