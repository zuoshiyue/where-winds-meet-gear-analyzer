<template>
  <div class="image-uploader">
    <el-upload
      ref="uploadRef"
      drag
      multiple
      :auto-upload="false"
      :on-change="handleFileChange"
      :on-remove="handleRemove"
      :file-list="fileList"
      accept="image/*"
      list-type="picture"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        拖拽截图到此处 或 <em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持批量上传，上传后点击"开始识别"按钮
        </div>
      </template>
    </el-upload>

    <div class="actions" v-if="fileList.length > 0">
      <el-button type="primary" @click="startOCR" :loading="isProcessing">
        {{ isProcessing ? '识别中...' : '开始识别' }}
      </el-button>
      <el-button @click="clearAll">清空</el-button>
    </div>

    <!-- 识别进度 -->
    <div class="progress" v-if="isProcessing">
      <el-progress 
        :percentage="progressPercent" 
        :status="progressStatus"
        :format="progressFormat"
      />
      <div class="log" v-if="ocrLogs.length > 0">
        <el-card>
          <div v-for="(log, index) in ocrLogs" :key="index" class="log-item">
            {{ log }}
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { createWorker } from 'tesseract.js'
import { parseEquipmentFromText } from '../utils/parser'
import { preprocessImage } from '../utils/preprocessor'

const emit = defineEmits(['upload-complete'])

const uploadRef = ref(null)
const fileList = ref([])
const isProcessing = ref(false)
const progressPercent = ref(0)
const progressStatus = ref('success')
const ocrLogs = ref([])

// 处理文件选择
const handleFileChange = (file, files) => {
  fileList.value = files
}

// 处理文件移除
const handleRemove = (file, files) => {
  fileList.value = files
}

// 清空所有
const clearAll = () => {
  fileList.value = []
  ocrLogs.value = []
  progressPercent.value = 0
}

// 开始 OCR 识别
const startOCR = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请先选择图片')
    return
  }

  isProcessing.value = true
  progressPercent.value = 0
  ocrLogs.value = []
  
  const equipments = []
  
  try {
    // 创建 OCR worker
    const worker = await createWorker('chi_sim', 1, {
      logger: m => {
        if (m.status === 'recognizing text') {
          progressPercent.value = Math.floor(m.progress * 100)
          ocrLogs.value.push(`识别中：${Math.floor(m.progress * 100)}%`)
        }
      }
    })

    // 逐张处理图片
    for (let i = 0; i < fileList.value.length; i++) {
      const file = fileList.value[i]
      ocrLogs.value.push(`正在处理 (${i + 1}/${fileList.value.length}): ${file.name}`)
      
      try {
        // 读取图片
        const img = await readFileAsImage(file.raw || file)
        
        // 预处理
        const processedImg = await preprocessImage(img)
        
        // OCR 识别
        const { data: { text } } = await worker.recognize(processedImg)
        
        ocrLogs.value.push(`识别完成：${text.substring(0, 50)}...`)
        
        // 解析装备数据
        const equipment = parseEquipmentFromText(text, file.name)
        if (equipment && equipment.name) {
          equipments.push(equipment)
          ocrLogs.value.push(`✓ 识别到装备：${equipment.name}`)
        } else {
          ocrLogs.value.push('⚠ 未识别到有效装备数据')
        }
      } catch (error) {
        ocrLogs.value.push(`✗ 处理失败：${error.message}`)
      }
      
      // 更新总进度
      progressPercent.value = Math.floor(((i + 1) / fileList.value.length) * 100)
    }

    await worker.terminate()

    if (equipments.length > 0) {
      ElMessage.success(`成功识别 ${equipments.length} 个装备`)
      emit('upload-complete', equipments)
    } else {
      ElMessage.warning('未识别到装备，请尝试上传更清晰的截图')
    }

  } catch (error) {
    console.error('OCR 错误:', error)
    ElMessage.error(`识别失败：${error.message}`)
    progressStatus.value = 'exception'
  } finally {
    isProcessing.value = false
  }
}

// 读取文件为 Image 对象
function readFileAsImage(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => resolve(img)
      img.onerror = reject
      img.src = e.target.result
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// 进度显示格式
const progressFormat = (percent) => {
  if (percent === 100) return '识别完成'
  return `${percent}%`
}
</script>

<style scoped>
.image-uploader {
  padding: 20px;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.progress {
  margin-top: 20px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.log {
  margin-top: 15px;
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  font-size: 13px;
  padding: 4px 0;
  border-bottom: 1px solid #eee;
}

.log-item:last-child {
  border-bottom: none;
}
</style>
