# 燕云装备助手 - Web 版

[![GitHub Pages](https://img.shields.io/badge/deploy-github%20pages-blue)](https://zuoshiyue.github.io/where-winds-meet-gear-analyzer)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/vite-5.x-purple)](https://vitejs.dev/)

> 🎮 燕云十六声装备分析工具 - 纯前端 Web 应用，无需后端，GitHub Pages 托管

**在线访问：** https://zuoshiyue.github.io/where-winds-meet-gear-analyzer

---

## ✨ 特性

- 🚀 **纯前端应用** - 无需安装，打开浏览器即用
- 📸 **截图上传** - 支持批量上传游戏截图
- 🔍 **OCR 识别** - 浏览器端文字识别，保护隐私
- 📊 **智能评分** - 基于职业和套装的装备评分系统
- 💾 **本地存储** - IndexedDB 存储，数据完全本地化
- 🎨 **响应式设计** - 支持桌面和移动端

---

## 🚀 快速开始

### 在线使用

直接访问：https://zuoshiyue.github.io/where-winds-meet-gear-analyzer

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/zuoshiyue/where-winds-meet-gear-analyzer.git
cd where-winds-meet-gear-analyzer/web

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 4. 构建生产版本
npm run build
```

---

## 📦 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Vue.js 3 |
| 构建工具 | Vite 5 |
| UI 组件 | Element Plus |
| OCR | Tesseract.js |
| 本地存储 | localforage (IndexedDB) |
| 图表 | ECharts |
| 部署 | GitHub Pages |

---

## 📖 功能说明

### 1. 截图上传
- 支持拖拽上传
- 批量上传多张截图
- 实时预览

### 2. OCR 识别
- 使用 Tesseract.js 进行中文识别
- 自动识别装备名称、属性、品质
- 识别结果可手动修正

### 3. 装备管理
- 装备列表展示
- 筛选 (品质、类型、套装)
- 排序 (评分、等级、品质)

### 4. 评分系统
- 职业配置 (输出/坦克/治疗)
- 属性权重自定义
- 评分详情展示

### 5. 数据统计
- 装备数量统计
- 品质分布图表
- 平均评分趋势

---

## 📁 项目结构

```
web/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── components/
│   │   ├── ImageUploader.vue      # 图片上传组件
│   │   ├── EquipmentList.vue      # 装备列表
│   │   ├── EquipmentDetail.vue    # 装备详情
│   │   ├── ScorePanel.vue         # 评分面板
│   │   └── StatsChart.vue         # 统计图表
│   ├── composables/
│   │   ├── useOCR.js              # OCR 逻辑
│   │   ├── useEquipment.js        # 装备管理
│   │   └── useStorage.js          # 本地存储
│   ├── utils/
│   │   ├── parser.js              # 数据解析
│   │   ├── scorer.js              # 评分逻辑
│   │   └── preprocessor.js        # 图像预处理
│   └── assets/
│       └── styles/
├── public/
│   └── tesseract/                 # Tesseract 语言数据
└── .github/
    └── workflows/
        └── deploy.yml             # GitHub Actions 部署
```

---

## 🔧 配置说明

### 职业配置

在 `src/utils/scorer.js` 中配置不同职业的属性权重：

```javascript
const CLASS_CONFIGS = {
  '输出': {
    attack: 1.2,
    crit: 1.8,
    crit_damage: 1.8,
  },
  '坦克': {
    defense: 1.8,
    health: 1.8,
  },
  // ...
}
```

### OCR 配置

在 `src/composables/useOCR.js` 中配置 Tesseract：

```javascript
const worker = await createWorker({
  logger: m => console.log(m),
});
await worker.loadLanguage('chi_sim');
await worker.initialize('chi_sim');
```

---

## 📝 开发指南

### 添加新功能

```bash
# 1. 创建新组件
# src/components/NewFeature.vue

# 2. 在 App.vue 中引入
# 3. 运行开发服务器测试
npm run dev
```

### 修改评分逻辑

编辑 `src/utils/scorer.js`，修改 `calculateScore` 函数。

### 添加新职业

在 `src/utils/scorer.js` 的 `CLASS_CONFIGS` 中添加新配置。

---

## 🌐 部署到 GitHub Pages

项目已配置自动部署，推送到 main 分支后自动构建发布。

手动部署：

```bash
# 安装 gh-pages
npm install -D gh-pages

# 构建
npm run build

# 部署
npx gh-pages -d dist
```

---

## ⚠️ 注意事项

1. **浏览器兼容性** - 需要支持 IndexedDB 的现代浏览器
2. **OCR 准确性** - 受截图质量影响，建议清晰截图
3. **数据备份** - 定期导出 CSV 备份数据
4. **隐私安全** - 所有数据处理在本地，不会上传服务器

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **GitHub:** https://github.com/zuoshiyue/where-winds-meet-gear-analyzer
- **Python 版本:** `/` (项目根目录保留 Python 代码作为参考)
- **Web 版本:** `/web`

---

**开发中...** 🚧
