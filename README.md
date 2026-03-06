# 燕云装备助手 (WhereWindsGear)

[![GitHub Pages](https://img.shields.io/badge/deploy-github%20pages-blue)](https://zuoshiyue.github.io/where-winds-meet-gear-analyzer)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green)](https://vuejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

> 🎮 燕云十六声装备分析工具 - 类似原神胡桃工具箱的装备评分和培养建议系统

**🌐 在线使用：** https://zuoshiyue.github.io/where-winds-meet-gear-analyzer

---

## ✨ 特性

### Web 版 (当前版本)
- 🚀 **纯前端应用** - 无需安装，打开浏览器即用
- 📸 **截图上传** - 支持批量上传游戏截图
- 🔍 **OCR 识别** - 浏览器端文字识别，保护隐私
- 📊 **智能评分** - 基于职业和套装的装备评分系统
- 💾 **本地存储** - IndexedDB 存储，数据完全本地化
- 🎨 **响应式设计** - 支持桌面和移动端
- 🔒 **独立运行** - 无需后端服务器，无需第三方服务

### Python 版 (历史版本/参考实现)
- 桌面应用版本 (PyQt6)
- 代码作为参考保留在 `/src` 目录

---

## 🛠️ 技术栈

### Web 版
| 类别 | 技术 |
|------|------|
| 框架 | Vue.js 3 |
| 构建工具 | Vite 5 |
| UI 组件库 | Element Plus |
| OCR | Tesseract.js |
| 本地存储 | localforage (IndexedDB) |
| 图表 | ECharts |
| 部署 | GitHub Pages |

### Python 版 (参考)
| 类别 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| OCR 引擎 | PaddleOCR |
| 图像处理 | OpenCV, Pillow |
| 截图库 | mss, PyAutoGUI |
| 数据库 | SQLite + SQLAlchemy |
| 数据分析 | pandas, numpy |
| UI | PyQt6 |

---

## 📁 项目结构

```
where-winds-meet-gear-analyzer/
├── README.md
├── web/                        # Web 版源码 (当前版本)
│   ├── src/
│   │   ├── components/         # Vue 组件
│   │   ├── composables/        # Composable 函数
│   │   ├── utils/              # 工具函数
│   │   ├── App.vue             # 主组件
│   │   └── main.js             # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── src/                        # Python 版源码 (参考)
│   ├── screenshot/             # 截图模块
│   ├── ocr/                    # OCR 模块
│   ├── database/               # 数据库模块
│   ├── analyzer/               # 分析模块
│   └── ui/                     # 界面模块
├── docs/                       # 文档
├── .github/
│   └── workflows/
│       └── deploy-web.yml      # GitHub Actions 部署
└── data/                       # 数据目录
    ├── screenshots/
    └── database/
```

---

## 🚀 快速开始

### 在线使用 (推荐)

直接访问：https://zuoshiyue.github.io/where-winds-meet-gear-analyzer/

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/zuoshiyue/where-winds-meet-gear-analyzer.git
cd where-winds-meet-gear-analyzer/web

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 4. 访问应用
# 打开浏览器：http://localhost:5173/
```

---

## 📖 功能说明

### 1. 截图上传
- 拖拽上传
- 批量上传
- 实时预览

### 2. OCR 识别
- Tesseract.js 中文识别
- 图像预处理 (去噪、增强对比度)
- 装备数据自动解析

### 3. 装备管理
- 装备列表展示
- 筛选 (品质、类型、套装)
- 排序 (评分、等级、品质)
- 删除装备

### 4. 评分系统
- 职业配置 (通用/输出/坦克)
- 属性权重自定义
- 评分详情展示
- 培养建议生成

### 5. 数据统计
- 装备数量统计
- 品质分布图表
- 类型分布图表
- 平均评分趋势

### 6. 数据管理
- 导出 JSON/CSV
- 导入备份数据
- 清空所有数据

---

## ⚠️ 注意事项

1. **浏览器兼容性** - 需要支持 IndexedDB 的现代浏览器 (Chrome 90+ / Edge 90+)
2. **OCR 准确性** - 受截图质量影响，建议上传清晰的游戏截图
3. **数据备份** - 定期导出 JSON 备份，清除浏览器缓存会丢失数据
4. **隐私安全** - 所有数据处理在本地完成，不会上传到任何服务器

---

## 📝 开发指南

### 添加新功能

```bash
# 1. 创建新组件
# web/src/components/NewFeature.vue

# 2. 在 App.vue 中引入
# 3. 运行开发服务器测试
npm run dev
```

### 修改评分逻辑

编辑 `web/src/utils/scorer.js`，修改 `calculateScore` 函数。

### 添加新职业

在 `web/src/utils/scorer.js` 的 `CLASS_CONFIGS` 中添加新配置。

---

## 🔗 相关链接

- **GitHub:** https://github.com/zuoshiyue/where-winds-meet-gear-analyzer
- **在线应用:** https://zuoshiyue.github.io/where-winds-meet-gear-analyzer/
- **Issue 追踪:** https://github.com/zuoshiyue/where-winds-meet-gear-analyzer/issues

---

## 📄 许可证

MIT License

---

**开发中...** 🚧
