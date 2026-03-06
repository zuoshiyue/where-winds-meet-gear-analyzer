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
            <el-collapse-item title="T0 破竹·鸢 ⚔️" name="1">
              <div class="config-item">
                <p><strong>武器：</strong>剑 + 扇</p>
                <p><strong>定位：</strong>极致爆发/无敌帧</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 ≈ 爆伤 > 速度</p>
                <p><strong>推荐理由：</strong>当前版本秒伤天花板，操作上限极高，竞速本必备</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T0 牵丝·玉 🏹" name="2">
              <div class="config-item">
                <p><strong>武器：</strong>弓 + 伞</p>
                <p><strong>定位：</strong>远程风筝/团队增益</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 > 精准</p>
                <p><strong>推荐理由：</strong>单刷最安全，组队最抢手，容错率与输出并存</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T0.5 破竹·风 ⚔️" name="3">
              <div class="config-item">
                <p><strong>武器：</strong>剑 + 刀</p>
                <p><strong>定位：</strong>高频吸血/持续压制</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 > 速度</p>
                <p><strong>推荐理由：</strong>生存能力优秀的输出流，低延迟下表现超越 T0</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T0.5 破竹·尘 🎵" name="4">
              <div class="config-item">
                <p><strong>武器：</strong>剑 + 笛</p>
                <p><strong>定位：</strong>强力控制/团队辅助</p>
                <p><strong>核心属性：</strong>攻击 > 元素 > 控制</p>
                <p><strong>推荐理由：</strong>高难副本必备辅助，能极大降低全队承伤压力</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T0.5 鸣金·影 🔱" name="5">
              <div class="config-item">
                <p><strong>武器：</strong>枪 + 剑</p>
                <p><strong>定位：</strong>流血爆发/近战缠斗</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 > 爆伤</p>
                <p><strong>推荐理由：</strong>喜欢近战操作感和高爆发数字的玩家首选</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T1 鸣金·虹 🏹" name="6">
              <div class="config-item">
                <p><strong>武器：</strong>枪 + 弓</p>
                <p><strong>定位：</strong>中距离拉扯/新手友好</p>
                <p><strong>核心属性：</strong>攻击 > 暴击 > 平衡</p>
                <p><strong>推荐理由：</strong>新手入坑首选，开荒体验极佳，几乎无短板</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T1 裂石·威 🛡️" name="7">
              <div class="config-item">
                <p><strong>武器：</strong>重剑 + 盾</p>
                <p><strong>定位：</strong>绝对防御/反击输出</p>
                <p><strong>核心属性：</strong>防御 > 生命 > 攻击</p>
                <p><strong>推荐理由：</strong>独狼玩家福音，面对高攻 BOSS 时生存率最高</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T1 裂石·钧 🔨" name="8">
              <div class="config-item">
                <p><strong>武器：</strong>重剑 + 锤</p>
                <p><strong>定位：</strong>超级破韧/眩晕控制</p>
                <p><strong>核心属性：</strong>防御 > 破韧 > 生命</p>
                <p><strong>推荐理由：</strong>适合对付霸体多、韧性高的巨型 BOSS</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T1 奇门·幻 🎭" name="9">
              <div class="config-item">
                <p><strong>武器：</strong>扇 + 笛</p>
                <p><strong>定位：</strong>诡异身法/异常状态</p>
                <p><strong>核心属性：</strong>元素 > 暴击 > 速度</p>
                <p><strong>推荐理由：</strong>PVP 强势，PVE 中适合处理特定机制怪</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="T2 游龙·水 💧" name="10">
              <div class="config-item">
                <p><strong>武器：</strong>刀 + 扇</p>
                <p><strong>定位：</strong>高机动/闪避反击</p>
                <p><strong>核心属性：</strong>速度 > 暴击 > 攻击</p>
                <p><strong>推荐理由：</strong>适合高手秀操作，普通玩家容易空大</p>
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
