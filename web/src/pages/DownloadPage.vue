<template>
  <div class="download-page">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🎮 燕云十六声 - 装备自动截图工具</h1>
          <p class="subtitle">一键自动捕获游戏内装备列表 · 配合网站 OCR 识别</p>
        </div>
      </el-header>

      <el-main>
        <div class="download-section">
          <!-- 下载卡片 -->
          <el-card class="download-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="title">📦 立即下载</span>
                <el-tag type="success" size="small">v1.0</el-tag>
              </div>
            </template>

            <div class="download-info">
              <div class="info-row">
                <span class="label">版本：</span>
                <span class="value">v1.0 (2026-03-06)</span>
              </div>
              <div class="info-row">
                <span class="label">大小：</span>
                <span class="value">~50 KB</span>
              </div>
              <div class="info-row">
                <span class="label">系统：</span>
                <span class="value">Windows 10/11</span>
              </div>
              <div class="info-row">
                <span class="label">环境：</span>
                <span class="value">Python 3.8+</span>
              </div>
            </div>

            <div class="download-buttons">
              <el-button
                type="primary"
                size="large"
                @click="downloadTool"
                class="download-btn"
              >
                <el-icon><Download /></el-icon>
                下载工具包
              </el-button>

              <el-button
                size="large"
                @click="openGitHub"
              >
                <el-icon><Link /></el-icon>
                GitHub 仓库
              </el-button>
            </div>

            <el-alert
              title="💡 首次使用？请看下方教程"
              type="info"
              show-icon
              :closable="false"
              class="tip-alert"
            />
          </el-card>

          <!-- 功能特性 -->
          <el-card class="features-card" shadow="hover">
            <template #header>
              <span class="title">✨ 功能特性</span>
            </template>

            <el-row :gutter="20">
              <el-col :span="12">
                <div class="feature-item">
                  <div class="feature-icon">⌨️</div>
                  <div class="feature-content">
                    <h4>热键截图</h4>
                    <p>按 F9 一键截图，简单快捷</p>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="feature-item">
                  <div class="feature-icon">🎯</div>
                  <div class="feature-content">
                    <h4>自动识别</h4>
                    <p>自动查找并锁定游戏窗口</p>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="feature-item">
                  <div class="feature-icon">📁</div>
                  <div class="feature-content">
                    <h4>智能命名</h4>
                    <p>截图自动按时间命名保存</p>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="feature-item">
                  <div class="feature-icon">⏱️</div>
                  <div class="feature-content">
                    <h4>定时模式</h4>
                    <p>可选定时自动截图</p>
                  </div>
                </div>
              </el-col>
            </el-row>
          </el-card>

          <!-- 使用教程 -->
          <el-card class="tutorial-card" shadow="hover">
            <template #header>
              <span class="title">📖 使用教程</span>
            </template>

            <el-timeline>
              <el-timeline-item timestamp="步骤 1" placement="top" type="primary">
                <el-card>
                  <h4>下载安装 Python</h4>
                  <p>下载并安装 Python 3.8 或更高版本</p>
                  <el-link
                    type="primary"
                    href="https://www.python.org/downloads/"
                    target="_blank"
                  >
                    前往下载 <el-icon><Link /></el-icon>
                  </el-link>
                </el-card>
              </el-timeline-item>

              <el-timeline-item timestamp="步骤 2" placement="top" type="primary">
                <el-card>
                  <h4>下载工具包</h4>
                  <p>点击上方"下载工具包"按钮，解压到任意目录</p>
                </el-card>
              </el-timeline-item>

              <el-timeline-item timestamp="步骤 3" placement="top" type="primary">
                <el-card>
                  <h4>安装依赖</h4>
                  <p>打开命令行，进入工具目录，运行：</p>
                  <el-code>pip install -r requirements.txt</el-code>
                </el-card>
              </el-timeline-item>

              <el-timeline-item timestamp="步骤 4" placement="top" type="primary">
                <el-card>
                  <h4>运行工具</h4>
                  <p>双击"快速启动.bat"或运行：</p>
                  <el-code>python auto_capture.py</el-code>
                </el-card>
              </el-timeline-item>

              <el-timeline-item timestamp="步骤 5" placement="top" type="primary">
                <el-card>
                  <h4>开始截图</h4>
                  <p>启动游戏，进入装备界面，按 <strong>F9</strong> 截图</p>
                </el-card>
              </el-timeline-item>

              <el-timeline-item timestamp="步骤 6" placement="top" type="success">
                <el-card>
                  <h4>上传识别</h4>
                  <p>将截图上传到网站，自动 OCR 识别装备属性</p>
                  <el-link
                    type="primary"
                    @click="$router.push('/')"
                  >
                    返回主页 <el-icon><Link /></el-icon>
                  </el-link>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <!-- 常见问题 -->
          <el-card class="faq-card" shadow="hover">
            <template #header>
              <span class="title">❓ 常见问题</span>
            </template>

            <el-collapse>
              <el-collapse-item title="提示"找不到游戏窗口"" name="1">
                <p>1. 确保游戏已启动</p>
                <p>2. 检查游戏窗口标题是否与配置一致</p>
                <p>3. 尝试修改 config.json 中的 game_window_title</p>
              </el-collapse-item>

              <el-collapse-item title="截图是黑屏" name="2">
                <p>全屏模式可能导致截图黑屏，建议：</p>
                <p>切换到窗口化或无边框窗口模式</p>
              </el-collapse-item>

              <el-collapse-item title="热键不响应" name="3">
                <p>1. 检查是否有其他程序占用该热键</p>
                <p>2. 修改 config.json 中的 capture_hotkey</p>
                <p>3. 以管理员身份运行工具</p>
              </el-collapse-item>

              <el-collapse-item title="如何在 Mac 上使用？" name="4">
                <p>当前版本仅支持 Windows，Mac 版本开发中</p>
              </el-collapse-item>

              <el-collapse-item title="是否安全？" name="5">
                <p>✅ 纯本地运行，不修改游戏文件</p>
                <p>✅ 不注入游戏进程，仅截图</p>
                <p>✅ 开源代码，透明可审查</p>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </div>
      </el-main>

      <el-footer>
        <div class="footer-content">
          <p>
            🛡️ 安全说明：本工具仅用于截图，不修改游戏文件，不影响游戏平衡
          </p>
          <p>
            由 <strong>OpenClaw AI</strong> 独立开发 | 
            <el-link
              type="primary"
              href="https://github.com/zuoshiyue/where-winds-meet-gear-analyzer"
              target="_blank"
            >
              GitHub 仓库
            </el-link>
          </p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { Download, Link } from '@element-plus/icons-vue'

// 下载工具包
const downloadTool = () => {
  // 创建 ZIP 下载
  // 实际部署时需要打包 tools 目录
  const downloadUrl = '/tools/燕云装备助手 - 自动截图工具-v1.0.zip'
  
  const a = document.createElement('a')
  a.href = downloadUrl
  a.download = '燕云装备助手 - 自动截图工具-v1.0.zip'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  
  // 显示提示
  alert('📦 下载即将开始！\n\n解压后请查看 README.md 了解详细使用说明')
}

// 打开 GitHub
const openGitHub = () => {
  window.open('https://github.com/zuoshiyue/where-winds-meet-gear-analyzer', '_blank')
}
</script>

<style scoped lang="scss">
.download-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 40px 20px;
  text-align: center;
  color: white;

  .header-content {
    max-width: 800px;
    margin: 0 auto;

    h1 {
      font-size: 32px;
      margin: 0 0 10px;
      font-weight: bold;
    }

    .subtitle {
      font-size: 16px;
      opacity: 0.9;
      margin: 0;
    }
  }
}

.el-main {
  padding: 40px 20px;
}

.download-section {
  max-width: 1000px;
  margin: 0 auto;

  .download-card {
    margin-bottom: 30px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .title {
        font-size: 18px;
        font-weight: bold;
      }
    }

    .download-info {
      margin: 20px 0;
      padding: 15px;
      background: #f5f7fa;
      border-radius: 8px;

      .info-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        
        &:last-child {
          margin-bottom: 0;
        }

        .label {
          color: #606266;
          font-weight: 500;
        }

        .value {
          color: #303133;
        }
      }
    }

    .download-buttons {
      display: flex;
      gap: 15px;
      margin-top: 20px;

      .download-btn {
        flex: 1;
        height: 50px;
        font-size: 16px;
      }
    }

    .tip-alert {
      margin-top: 20px;
    }
  }

  .features-card {
    margin-bottom: 30px;

    .feature-item {
      display: flex;
      align-items: center;
      padding: 15px;
      margin-bottom: 15px;
      background: #f5f7fa;
      border-radius: 8px;
      transition: transform 0.3s;

      &:hover {
        transform: translateY(-3px);
      }

      &:last-child {
        margin-bottom: 0;
      }

      .feature-icon {
        font-size: 36px;
        margin-right: 15px;
      }

      .feature-content {
        h4 {
          margin: 0 0 5px;
          color: #303133;
          font-size: 16px;
        }

        p {
          margin: 0;
          color: #606266;
          font-size: 14px;
        }
      }
    }
  }

  .tutorial-card {
    margin-bottom: 30px;

    :deep(.el-timeline-item__content) {
      .el-card {
        h4 {
          margin: 0 0 10px;
          color: #303133;
        }

        p {
          margin: 0 0 10px;
          color: #606266;
          line-height: 1.6;
        }

        el-code {
          display: block;
          padding: 10px;
          background: #f5f7fa;
          border-radius: 4px;
          font-family: 'Courier New', monospace;
          color: #409EFF;
        }
      }
    }
  }

  .faq-card {
    :deep(.el-collapse-item__header) {
      font-size: 15px;
      font-weight: 500;
    }

    :deep(.el-collapse-item__content) {
      p {
        margin: 5px 0;
        color: #606266;
        line-height: 1.6;
      }
    }
  }
}

.el-footer {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  text-align: center;
  color: white;

  .footer-content {
    max-width: 800px;
    margin: 0 auto;

    p {
      margin: 5px 0;
      font-size: 14px;
      opacity: 0.9;
    }
  }
}
</style>
