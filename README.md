# 燕云十六声装备分析工具 - 需求文档

## 📋 项目概述

**项目名称：** 燕云十六声装备分析工具 (Where Winds Meet Gear Analyzer)  
**项目类型：** 游戏装备管理工具  
**参考项目：** 原神胡桃工具箱 (Hutao)  
**目标用户：** 燕云十六声 PC 端玩家

---

## 🎯 核心功能

### 1. 截图采集模块
- **自动截图：** 监听游戏窗口，定时/触发式截图
- **手动截图：** 快捷键触发截图 (默认 F12)
- **区域识别：** 自动识别背包界面区域
- **图像预处理：** 去噪、增强、裁剪

### 2. OCR 识别模块
- **装备名称识别：** 中文装备名称提取
- **属性识别：** 
  - 基础属性 (攻击、防御、生命等)
  - 附加属性 (暴击、爆伤、元素伤害等)
  - 强化等级
- **品质识别：** 颜色识别 (白/绿/蓝/紫/金)
- **套装识别：** 套装名称和套装效果

### 3. 数据存储模块
- **本地数据库：** SQLite 存储装备数据
- **飞书集成：** 同步到飞书 Bitable (可选)
- **截图管理：** 截图与数据关联存储
- **导出功能：** Excel/CSV 导出

### 4. 评分分析模块
- **职业配置：** 
  - 不同职业的装备偏好
  - 套装适配度
  - 属性权重
- **评分系统：**
  - 单件装备评分
  - 套装整体评分
  - 培养价值评估
- **对比功能：** 装备对比、替换建议

### 5. 用户界面
- **主界面：** 装备列表、筛选、排序
- **详情页：** 装备详情、属性图表
- **分析页：** 评分结果、培养建议
- **设置页：** 职业配置、OCR 设置、快捷键

---

## 🛠️ 技术栈

### 后端
- **语言：** Python 3.10+
- **OCR 引擎：** PaddleOCR (中文识别优化)
- **图像处理：** OpenCV, Pillow
- **截图库：** mss, PyAutoGUI
- **数据库：** SQLite + SQLAlchemy
- **数据分析：** pandas, numpy

### 前端 (可选)
- **框架：** Electron + React 或 PyQt6
- **UI 库：** Ant Design 或 PyQt 原生组件
- **图表：** ECharts / Chart.js

### 集成
- **飞书 API：** Bitable 数据同步
- **GitHub：** 代码托管、Issue 追踪

---

## 📁 项目结构

```
where-winds-meet-gear-analyzer/
├── README.md
├── requirements.txt
├── config.yaml                 # 配置文件
├── main.py                     # 主入口
├── src/
│   ├── __init__.py
│   ├── screenshot/            # 截图模块
│   │   ├── __init__.py
│   │   ├── capture.py         # 截图功能
│   │   └── region.py          # 区域识别
│   ├── ocr/                   # OCR 模块
│   │   ├── __init__.py
│   │   ├── recognizer.py      # OCR 识别
│   │   ├── parser.py          # 数据解析
│   │   └── preprocessor.py    # 图像预处理
│   ├── database/              # 数据库模块
│   │   ├── __init__.py
│   │   ├── models.py          # 数据模型
│   │   ├── repository.py      # 数据操作
│   │   └── feishu_sync.py     # 飞书同步
│   ├── analyzer/              # 分析模块
│   │   ├── __init__.py
│   │   ├── scorer.py          # 评分系统
│   │   ├── classifier.py      # 职业分类
│   │   └── recommender.py     # 培养建议
│   └── ui/                    # 界面模块
│       ├── __init__.py
│       ├── main_window.py     # 主窗口
│       └── components/        # UI 组件
├── data/
│   ├── screenshots/           # 截图存储
│   ├── database/              # 数据库文件
│   └── config/                # 用户配置
├── docs/
│   ├── 开发文档.md
│   ├── API 文档.md
│   └── 使用指南.md
└── tests/                     # 测试用例
    ├── test_ocr.py
    ├── test_analyzer.py
    └── test_database.py
```

---

## 📊 数据模型

### 装备表 (Equipment)
```sql
- id: INTEGER PRIMARY KEY
- name: TEXT                  # 装备名称
- type: TEXT                  # 装备类型 (武器/防具/饰品)
- quality: INTEGER            # 品质 (1-5)
- level: INTEGER              # 强化等级
- set_name: TEXT              # 套装名称
- stats: JSON                 # 属性列表
- screenshot_path: TEXT       # 截图路径
- created_at: DATETIME
- updated_at: DATETIME
```

### 职业配置表 (ClassConfig)
```sql
- id: INTEGER PRIMARY KEY
- class_name: TEXT            # 职业名称
- preferred_sets: JSON        # 推荐套装
- stat_weights: JSON          # 属性权重
- notes: TEXT                 # 备注
```

### 评分记录表 (ScoreRecord)
```sql
- id: INTEGER PRIMARY KEY
- equipment_id: INTEGER       # 装备 ID
- class_name: TEXT            # 职业名称
- total_score: FLOAT          # 总分
- sub_scores: JSON            # 分项评分
- recommendation: TEXT        # 培养建议
- created_at: DATETIME
```

---

## 🎨 UI 设计要点

### 主界面布局
```
┌─────────────────────────────────────┐
│  工具栏 [截图] [分析] [导出] [设置]   │
├─────────────┬───────────────────────┤
│             │                       │
│  筛选面板   │      装备列表          │
│  - 职业     │   (表格/卡片视图)      │
│  - 品质     │                       │
│  - 类型     │                       │
│  - 套装     │                       │
│             │                       │
├─────────────┴───────────────────────┤
│  状态栏 [装备数：123] [最后更新：...] │
└─────────────────────────────────────┘
```

### 装备详情页
- 装备大图展示
- 属性列表 (高亮核心属性)
- 评分雷达图
- 培养建议文本
- 对比功能入口

---

## 📈 开发里程碑

### Phase 1 - 核心功能 (2 周)
- [x] 项目初始化
- [ ] 截图功能实现
- [ ] OCR 识别基础功能
- [ ] 数据库模型设计
- [ ] 基础 UI 框架

### Phase 2 - 数据分析 (2 周)
- [ ] 装备属性解析完善
- [ ] 评分系统实现
- [ ] 职业配置系统
- [ ] 飞书集成

### Phase 3 - 优化完善 (1 周)
- [ ] UI 优化
- [ ] 性能优化
- [ ] 测试用例
- [ ] 文档完善

### Phase 4 - 扩展功能 (可选)
- [ ] 自动批量截图
- [ ] 装备交易价值评估
- [ ] 社区分享功能
- [ ] 多游戏支持

---

## ⚠️ 注意事项

1. **游戏合规性：** 仅用于个人数据分析，不涉及游戏修改
2. **OCR 准确性：** 需要大量样本训练优化
3. **性能优化：** 截图和 OCR 较耗资源，需优化
4. **数据安全：** 本地存储优先，云端同步可选

---

## 📚 参考资料

- [原神胡桃工具箱](https://github.com/DGP-Studio/Hutao) - 参考 UI 和评分系统
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 中文 OCR 引擎
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - 自动化控制
- [飞书开放平台](https://open.feishu.cn/) - 数据同步 API

---

**创建日期：** 2026-03-06  
**版本：** v1.0  
**状态：** 开发中
