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
            <el-collapse-item title="鸣金·虹 🔱" name="1">
              <div class="config-item">
                <p><strong>武器：</strong>无名剑法 + 无名枪法</p>
                <p><strong>定位：</strong>中远程均衡输出</p>
                <p><strong>核心属性：</strong>外功攻击 > 精准率 > 会心率/会意率</p>
                <p><strong>毕业面板：</strong>外攻 3800+，精准 95%+，会心 38%+，会意 39%+</p>
                <p><strong>推荐理由：</strong>攻守兼备的万金油选择，剑气与枪芒交织</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="鸣金·影 ⚔️" name="2">
              <div class="config-item">
                <p><strong>武器：</strong>积矩九剑 + 九曲惊神枪</p>
                <p><strong>定位：</strong>近战流血爆发</p>
                <p><strong>核心属性：</strong>外功攻击 > 精准率 > 会心率/会意率</p>
                <p><strong>毕业面板：</strong>外攻 3800+，精准 97%+，会心 45%+，会意 37%+</p>
                <p><strong>推荐理由：</strong>九剑叠加流血，枪引爆爆发，节奏感极强</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="裂石·威 🛡️" name="3">
              <div class="config-item">
                <p><strong>武器：</strong>嗟夫刀法 + 八方风雷枪</p>
                <p><strong>定位：</strong>坦克/近战输出</p>
                <p><strong>核心属性：</strong>外功攻击 > 精准率 > 会心率</p>
                <p><strong>毕业面板：</strong>外攻 1600-3300，精准 98%+，会心 56%+</p>
                <p><strong>推荐理由：</strong>嗟夫刀减伤，八方枪控制，团队前排</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="破竹·风 💨" name="4">
              <div class="config-item">
                <p><strong>武器：</strong>泥犁三垢 + 粟子游尘</p>
                <p><strong>定位：</strong>近战高机动刺客</p>
                <p><strong>核心属性：</strong>外功攻击 > 精准率 > 会心率</p>
                <p><strong>毕业面板：</strong>外攻 1700-3400，精准 98%+，会心 65%+</p>
                <p><strong>推荐理由：</strong>毒伤 + 灵动位移，专攻敌方弱点</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="破竹·鸢 🦅" name="5">
              <div class="config-item">
                <p><strong>武器：</strong>天志垂象 + 千机锁天</p>
                <p><strong>定位：</strong>全能型控制/输出</p>
                <p><strong>核心属性：</strong>会心率/会意率 > 外功攻击 > 精准率</p>
                <p><strong>毕业面板：</strong>会心 50%+，会意 40%+，外攻尽可能高</p>
                <p><strong>推荐理由：</strong>霸体硬刚 + 远程拉扯，战场适应性极强</p>
              </div>
            </el-collapse-item>
            <el-collapse-item title="牵丝·霖 🌧️" name="6">
              <div class="config-item">
                <p><strong>武器：</strong>明川药典 + 千香引魂蛊</p>
                <p><strong>定位：</strong>纯治疗辅助</p>
                <p><strong>核心属性：</strong>鸣金攻击 > 会心率 > 牵丝攻击</p>
                <p><strong>毕业面板：</strong>外攻 1700-3400，会心 75%+，牵丝 850+</p>
                <p><strong>推荐理由：</strong>群体治疗 + 净化，团队生存保障</p>
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
