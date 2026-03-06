@echo off
chcp 65001 >nul
title 燕云十六声 - 装备批量扫描工具

echo ================================================
echo   燕云十六声 - 装备批量扫描工具
echo   自动 OCR 识别背包装备并导出 JSON
echo ================================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到 Python 环境
    echo.
    echo 请先安装 Python 3.8 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python 环境检测通过
python --version
echo.

:: 检查 Tesseract-OCR 是否安装
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 未检测到 Tesseract-OCR
    echo.
    echo 请先安装 Tesseract-OCR
    echo 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo 安装后请编辑 equipment_scanner.py
    echo 取消注释并修改 tesseract_cmd 路径
    echo.
    pause
    exit /b 1
)

echo ✅ Tesseract-OCR 检测通过
tesseract --version
echo.

:: 检查依赖是否安装
echo 🔍 检查依赖库...
python -c "import pytesseract" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 未找到必要依赖库
    echo.
    echo 正在自动安装依赖...
    echo.
    pip install -r requirements_scanner.txt
    if %errorlevel% neq 0 (
        echo.
        echo ❌ 依赖安装失败
        echo.
        echo 请手动运行：pip install -r requirements_scanner.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo ✅ 依赖安装完成
    echo.
) else (
    echo ✅ 依赖库检查通过
    echo.
)

:: 启动工具
echo 🚀 启动工具...
echo.
echo 💡 使用说明:
echo   - F10: 扫描当前装备列表
echo   - F11: 批量导入截图
echo   - F12: 导出 JSON 文件
echo   - 鼠标移到屏幕左上角可紧急停止
echo   - Ctrl+C 退出程序
echo.
echo ================================================
echo.

python equipment_scanner.py

pause
