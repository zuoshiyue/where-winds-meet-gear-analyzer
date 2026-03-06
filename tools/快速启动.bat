@echo off
chcp 65001 >nul
title 燕云十六声 - 装备自动截图工具

echo ================================================
echo   燕云十六声 - 装备自动截图工具
echo   燕云装备助手配套工具
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

:: 检查依赖是否安装
echo 🔍 检查依赖库...
python -c "import pyautogui" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 未找到必要依赖库
    echo.
    echo 正在自动安装依赖...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ❌ 依赖安装失败
        echo.
        echo 请手动运行：pip install -r requirements.txt
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
echo   - 按 F9 截图游戏窗口
echo   - 鼠标移到屏幕左上角可紧急停止
echo   - 按 Ctrl+C 退出程序
echo.
echo ================================================
echo.

python auto_capture.py

pause
