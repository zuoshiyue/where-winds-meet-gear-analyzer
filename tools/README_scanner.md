# 🎮 燕云十六声 - 装备批量扫描工具

**燕云装备助手配套工具** - 自动 OCR 识别背包装备并导出 JSON

---

## 📦 功能特性

### ✨ 核心功能
- ✅ **批量截图** - 一键捕获背包装备列表
- ✅ **OCR 识别** - 自动识别装备名称、品质、词条
- ✅ **JSON 导出** - 生成网站兼容的导入格式
- ✅ **批量处理** - 支持导入多张截图批量识别
- ✅ **图像增强** - 自动预处理提升 OCR 识别率

### 🛡️ 安全特性
- ✅ 纯本地运行，不修改游戏文件
- ✅ 不注入游戏进程，仅截图 +OCR
- ✅ 开源代码，透明可审查
- ✅ 紧急停止功能（鼠标移左上角）

---

## 🚀 快速开始

### 步骤 1：安装 Python 环境

**需要 Python 3.8 或更高版本**

```bash
python --version  # 验证安装
```

### 步骤 2：安装 Tesseract-OCR

**Windows 用户：**
1. 下载：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装 Tesseract-OCR v5.x
3. 记住安装路径（默认：`C:\Program Files\Tesseract-OCR`）

**Mac 用户：**
```bash
brew install tesseract
```

**Linux 用户：**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

### 步骤 3：安装 Python 依赖

```bash
cd tools
pip install -r requirements_scanner.txt
```

### 步骤 4：配置 Tesseract 路径（Windows）

编辑 `equipment_scanner.py`，找到以下行并取消注释：

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 步骤 5：运行工具

```bash
python equipment_scanner.py
```

### 步骤 6：开始扫描

1. 启动游戏《燕云十六声》
2. 打开背包/装备界面
3. 按 **F10** 扫描当前装备列表
4. 按 **F11** 从文件夹导入截图批量处理
5. 按 **F12** 导出 JSON 文件
6. 截图和 JSON 保存到 `scans/` 目录

---

## ⌨️ 热键说明

| 热键 | 功能 | 说明 |
|------|------|------|
| **F10** | 扫描装备列表 | 截取当前游戏窗口并 OCR 识别 |
| **F11** | 批量导入截图 | 从 `scans/` 文件夹导入所有截图批量处理 |
| **F12** | 导出 JSON | 导出识别结果为网站兼容格式 |
| **Ctrl+C** | 退出程序 | 自动保存并退出 |
| **鼠标左上角** | 紧急停止 | 移到屏幕左上角立即停止 |

---

## 📊 输出格式

### JSON 文件结构

```json
{
  "version": "1.0",
  "export_time": "2026-03-06T18:40:00",
  "tool": "燕云装备助手 - 批量扫描工具",
  "equipment_count": 10,
  "equipment_list": [
    {
      "name": "无名剑",
      "quality": 5,
      "level": 15,
      "set_name": "无名套装",
      "stats": [
        {
          "type": "unknown",
          "value": "最大外功攻击 +85",
          "raw": "最大外功攻击 +85"
        }
      ],
      "image_path": "scans/equip_list_20260306_184000.png",
      "scan_time": "2026-03-06T18:40:00",
      "raw_text": "识别的原始文本"
    }
  ]
}
```

### 网站导入

1. 打开燕云装备助手网站
2. 点击"📥 导入 JSON"
3. 选择导出的 `equipment_export.json`
4. 装备数据自动导入到网站

---

## 💡 使用技巧

### 1. 提高 OCR 识别率

**游戏设置建议：**
- 使用**窗口化**或**无边框窗口**模式
- 调高 UI 缩放比例（120%-150%）
- 使用清晰的字体
- 避免过度复杂的背景

**截图建议：**
- 确保装备列表完整显示
- 避免遮挡和反光
- 保持界面整洁

### 2. 批量扫描流程

```
1. 游戏中打开背包
2. F10 截图第一页
3. 翻页 → F10 截图第二页
4. 重复直到所有装备截图完成
5. F11 批量导入所有截图
6. F12 导出 JSON
7. 网站导入 JSON
```

### 3. 手动修正识别结果

如果 OCR 识别不准确：
1. 打开导出的 JSON 文件
2. 手动修正 `name`、`stats` 等字段
3. 保存后导入网站

### 4. 图像预处理

工具会自动进行：
- ✅ 灰度转换
- ✅ 二值化增强对比度
- ✅ 降噪处理

如需调整，编辑 `preprocess_image()` 函数

---

## 🔧 常见问题

### Q1: pytesseract 报错 "Tesseract NotFoundError"

**原因：** 未安装 Tesseract-OCR 或路径配置错误

**解决方法：**
```bash
# Windows: 检查安装路径
# 编辑 equipment_scanner.py，取消注释并修改路径：
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Q2: OCR 识别结果为空或乱码

**原因：** 图像质量差或语言包缺失

**解决方法：**
1. 安装中文语言包：
   ```bash
   # Windows: 下载时勾选 Chinese Simplified
   # Mac:
   brew install tesseract-lang
   ```
2. 调高游戏 UI 缩放
3. 确保截图清晰

### Q3: 识别准确率不高

**优化建议：**
1. 使用窗口化模式
2. 调高 UI 缩放（120%-150%）
3. 截图时确保装备列表完整
4. 手动修正识别结果

### Q4: 如何自定义识别规则？

**编辑 `parse_equipment_info()` 函数：**

```python
def parse_equipment_info(self, ocr_text: str) -> Dict[str, Any]:
    # 添加自定义解析逻辑
    # 例如：识别特定词条格式
```

---

## 📁 目录结构

```
tools/
├── equipment_scanner.py       # 主程序
├── scanner_config.json        # 配置文件（首次运行自动生成）
├── requirements_scanner.txt   # Python 依赖
├── README_scanner.md          # 使用说明（本文件）
├── scanner.log                # 运行日志
└── scans/                     # 输出目录
    ├── equip_list_20260306_184000.png
    ├── equip_list_20260306_184100.png
    └── equipment_export.json  # 导出的 JSON 文件
```

---

## 🌐 网站集成

### 导入 JSON 到网站

1. 打开燕云装备助手网站
2. 点击"📥 导入 JSON"按钮
3. 选择 `scans/equipment_export.json`
4. 装备自动导入到网站数据库

### JSON 格式要求

```json
{
  "version": "1.0",
  "equipment_list": [
    {
      "name": "装备名称",
      "quality": 1-5,
      "level": 0-20,
      "set_name": "套装名称",
      "stats": [
        {
          "type": "属性类型",
          "value": "属性值"
        }
      ]
    }
  ]
}
```

---

## 🛡️ 安全说明

### 本工具不会：
- ❌ 修改游戏文件
- ❌ 注入游戏进程
- ❌ 修改游戏内存
- ❌ 自动操作游戏（仅截图）
- ❌ 收集个人信息

### 本工具会：
- ✅ 截取游戏窗口图像
- ✅ 使用 OCR 识别图像文字
- ✅ 保存为本地图片和 JSON 文件
- ✅ 记录运行日志

---

## 📝 更新日志

### v1.0 (2026-03-06)
- ✅ 初始版本发布
- ✅ 批量截图功能
- ✅ OCR 识别装备信息
- ✅ JSON 导出功能
- ✅ 图像预处理增强
- ✅ 热键控制

---

## 📞 反馈与支持

### 遇到问题？

1. **查看日志文件** - `scanner.log`
2. **查看常见问题** - 本文件 "常见问题" 章节
3. **提交 Issue** - GitHub 仓库
4. **联系作者** - 网站反馈渠道

### GitHub 仓库

https://github.com/zuoshiyue/where-winds-meet-gear-analyzer

---

## 📄 开源协议

MIT License - 开源免费使用

---

## 🙏 致谢

感谢使用燕云装备助手！

**工具由 OpenClaw AI 独立开发**

---

**最后更新：** 2026-03-06  
**版本：** v1.0  
**作者：** 燕云装备助手团队
