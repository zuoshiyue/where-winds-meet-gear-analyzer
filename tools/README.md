# 🎮 燕云十六声 - 装备自动截图工具

**燕云装备助手配套工具** - 一键自动捕获游戏内装备列表

---

## 📦 功能特性

### ✨ 核心功能
- ✅ **热键截图** - 按 F9 一键截图游戏窗口
- ✅ **自动识别** - 自动查找并锁定游戏窗口
- ✅ **智能命名** - 截图自动按时间命名
- ✅ **定时模式** - 可选定时自动截图
- ✅ **自动上传** - 可选自动上传到网站（开发中）

### 🛡️ 安全特性
- ✅ 纯本地运行，不修改游戏文件
- ✅ 不注入游戏进程，仅截图
- ✅ 开源代码，透明可审查
- ✅ 紧急停止功能（鼠标移到屏幕左上角）

---

## 🚀 快速开始

### 步骤 1：下载工具

**方式 A：直接下载（推荐）**
```
访问网站下载页面 → 点击下载 → 解压到任意目录
```

**方式 B：Git 克隆**
```bash
git clone https://github.com/zuoshiyue/where-winds-meet-gear-analyzer.git
cd where-winds-meet-gear-analyzer/tools
```

### 步骤 2：安装 Python 环境

**需要 Python 3.8 或更高版本**

1. 下载 Python: https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 验证安装：
   ```bash
   python --version
   ```

### 步骤 3：安装依赖

打开命令行（CMD 或 PowerShell），进入工具目录：
```bash
cd 工具所在目录
pip install -r requirements.txt
```

### 步骤 4：运行工具

```bash
python auto_capture.py
```

### 步骤 5：开始截图

1. 启动游戏《燕云十六声》
2. 进入装备界面
3. 按 **F9** 截图
4. 截图保存到 `captures/` 目录

---

## ⚙️ 配置说明

### 配置文件

首次运行会自动生成 `config.json`，可以自定义配置：

```json
{
  "game_window_title": "燕云十六声",
  "capture_hotkey": "f9",
  "output_dir": "captures",
  "auto_upload": false,
  "upload_url": "",
  "timer_mode": false,
  "timer_interval": 30,
  "image_format": "png",
  "image_quality": 95
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `game_window_title` | 游戏窗口标题 | "燕云十六声" |
| `capture_hotkey` | 截图热键 | "f9" |
| `output_dir` | 截图保存目录 | "captures" |
| `auto_upload` | 是否自动上传 | false |
| `upload_url` | 上传 API 地址 | "" |
| `timer_mode` | 定时截图模式 | false |
| `timer_interval` | 定时截图间隔（秒） | 30 |
| `image_format` | 图片格式 | "png" |
| `image_quality` | JPG 质量（1-100） | 95 |

### 可用热键

支持的热键示例：
- 功能键：`f1` - `f12`
- 打印键：`print_screen`, `prtsc`
- 组合键：`ctrl+shift+s`, `alt+f9`

---

## 💡 使用技巧

### 1. 窗口模式建议

**推荐使用窗口化或无边框窗口模式**

```
游戏设置 → 显示设置 → 屏幕模式 → 窗口化/无边框窗口
```

全屏模式可能导致：
- 截图黑屏
- 切换窗口卡顿

### 2. 截图工作流

```
1. 启动游戏
2. 运行工具（python auto_capture.py）
3. 进入装备界面
4. 按 F9 截图
5. 查看 captures/ 目录
6. 上传到网站进行 OCR 识别
```

### 3. 定时截图模式

适合批量采集装备数据：

```json
{
  "timer_mode": true,
  "timer_interval": 30
}
```

⚠️ 注意：定时模式下需要手动切换装备界面

### 4. 紧急停止

**鼠标移到屏幕左上角** 可立即停止工具

这是 pyautogui 的安全机制，防止程序失控

---

## 📁 目录结构

```
tools/
├── auto_capture.py          # 主程序
├── config.json              # 配置文件（首次运行自动生成）
├── config.example.json      # 配置示例
├── requirements.txt         # Python 依赖
├── README.md                # 使用说明（本文件）
├── auto_capture.log         # 运行日志（运行后生成）
└── captures/                # 截图保存目录
    ├── equip_20260306_143022.png
    ├── equip_20260306_143156.png
    └── ...
```

---

## 🔧 常见问题

### Q1: 提示 "找不到游戏窗口"

**解决方法：**
1. 确保游戏已启动
2. 检查游戏窗口标题是否与配置一致
3. 尝试手动修改 `config.json` 中的 `game_window_title`

### Q2: 截图是黑屏

**原因：** 全屏模式可能导致截图黑屏

**解决方法：**
1. 切换到窗口化或无边框窗口模式
2. 重启工具后重试

### Q3: 热键不响应

**解决方法：**
1. 检查是否有其他程序占用该热键
2. 修改 `config.json` 中的 `capture_hotkey`
3. 以管理员身份运行工具

### Q4: 依赖安装失败

**解决方法：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q5: 如何在 Mac 上使用？

⚠️ **当前版本仅支持 Windows**

Mac 版本开发中，需要：
- 替换 `pygetwindow` 为 `pywinctl`
- 调整窗口捕获逻辑

---

## 🌐 自动上传功能（开发中）

### 配置自动上传

```json
{
  "auto_upload": true,
  "upload_url": "https://your-website.com/api/upload"
}
```

### 上传流程

```
截图 → 保存 → 自动上传 → 网站 OCR 识别 → 返回结果
```

⚠️ 注意：此功能需要网站支持上传 API

---

## 📝 更新日志

### v1.0 (2026-03-06)
- ✅ 初始版本发布
- ✅ 热键截图功能
- ✅ 自动窗口识别
- ✅ 定时截图模式
- ✅ 配置文件支持
- ✅ 日志记录功能

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
- ✅ 保存为本地图片文件
- ✅ 记录运行日志
- ✅ （可选）上传截图到指定网站

---

## 📞 反馈与支持

### 遇到问题？

1. **查看日志文件** - `auto_capture.log`
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
