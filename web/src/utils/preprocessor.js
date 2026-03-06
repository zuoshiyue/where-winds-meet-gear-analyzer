/**
 * 图像预处理模块
 * 使用 Canvas 进行图像增强，提高 OCR 识别率
 */

/**
 * 预处理图像
 * @param {HTMLImageElement} img - 输入图像
 * @param {Object} options - 预处理选项
 * @returns {HTMLCanvasElement} 处理后的图像
 */
export function preprocessImage(img, options = {}) {
  const {
    denoise = true,
    enhanceContrast = true,
    binarize = false,
    blurKernel = 3,
  } = options

  // 创建 Canvas
  const canvas = document.createElement('canvas')
  canvas.width = img.width
  canvas.height = img.height
  const ctx = canvas.getContext('2d')

  // 绘制原始图像
  ctx.drawImage(img, 0, 0)

  // 获取图像数据
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const data = imageData.data

  // 去噪
  if (denoise) {
    applyDenoise(data, canvas.width, canvas.height, blurKernel)
  }

  // 增强对比度
  if (enhanceContrast) {
    enhanceContrastHistogram(data)
  }

  // 二值化
  if (binarize) {
    applyBinarize(data, 128)
  }

  // 放回 Canvas
  ctx.putImageData(imageData, 0, 0)

  return canvas
}

/**
 * 简单去噪 (均值滤波)
 */
function applyDenoise(data, width, height, kernelSize) {
  const copy = new Uint8ClampedArray(data)
  const halfKernel = Math.floor(kernelSize / 2)

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let sumR = 0, sumG = 0, sumB = 0, count = 0

      for (let ky = -halfKernel; ky <= halfKernel; ky++) {
        for (let kx = -halfKernel; kx <= halfKernel; kx++) {
          const px = x + kx
          const py = y + ky

          if (px >= 0 && px < width && py >= 0 && py < height) {
            const idx = (py * width + px) * 4
            sumR += copy[idx]
            sumG += copy[idx + 1]
            sumB += copy[idx + 2]
            count++
          }
        }
      }

      const idx = (y * width + x) * 4
      data[idx] = sumR / count
      data[idx + 1] = sumG / count
      data[idx + 2] = sumB / count
    }
  }
}

/**
 * 增强对比度 (直方图均衡化简化版)
 */
function enhanceContrastHistogram(data) {
  // 转换为灰度并计算直方图
  const histogram = new Array(256).fill(0)
  
  for (let i = 0; i < data.length; i += 4) {
    const gray = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2])
    histogram[gray]++
  }

  // 计算累积分布函数
  const cdf = new Array(256).fill(0)
  cdf[0] = histogram[0]
  for (let i = 1; i < 256; i++) {
    cdf[i] = cdf[i - 1] + histogram[i]
  }

  // 归一化 CDF
  const total = data.length / 4
  const cdfMin = cdf.find(val => val > 0) || 1
  const scale = 255 / (total - cdfMin)

  // 创建查找表
  const lut = new Array(256)
  for (let i = 0; i < 256; i++) {
    lut[i] = Math.round((cdf[i] - cdfMin) * scale)
  }

  // 应用对比度增强
  for (let i = 0; i < data.length; i += 4) {
    const gray = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2])
    const enhanced = lut[gray]
    
    // 按比例增强 RGB
    const ratio = enhanced / (gray || 1)
    data[i] = Math.min(255, Math.round(data[i] * ratio))
    data[i + 1] = Math.min(255, Math.round(data[i + 1] * ratio))
    data[i + 2] = Math.min(255, Math.round(data[i + 2] * ratio))
  }
}

/**
 * 二值化
 */
function applyBinarize(data, threshold) {
  for (let i = 0; i < data.length; i += 4) {
    const gray = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2])
    const value = gray >= threshold ? 255 : 0
    data[i] = value
    data[i + 1] = value
    data[i + 2] = value
  }
}

/**
 * 裁剪图像区域
 */
export function cropImage(img, region) {
  const [x, y, width, height] = region
  
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')
  
  ctx.drawImage(img, x, y, width, height, 0, 0, width, height)
  
  return canvas
}

/**
 * 调整图像大小
 */
export function resizeImage(img, maxWidth, maxHeight) {
  let width = img.width
  let height = img.height

  // 计算缩放比例
  let scale = 1
  if (width > maxWidth || height > maxHeight) {
    scale = Math.min(maxWidth / width, maxHeight / height)
  }

  const newWidth = Math.floor(width * scale)
  const newHeight = Math.floor(height * scale)

  const canvas = document.createElement('canvas')
  canvas.width = newWidth
  canvas.height = newHeight
  const ctx = canvas.getContext('2d')

  ctx.drawImage(img, 0, 0, newWidth, newHeight)

  return canvas
}
