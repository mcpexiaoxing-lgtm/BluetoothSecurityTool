@echo off
chcp 65001 >nul
echo ============================================
echo IoT蓝牙安全测试工具 - 本地构建脚本
echo ============================================
echo.

cd /d "%~dp0"

echo [1/5] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python！
    echo 请先安装Python 3.8-3.12：https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python已安装
python --version
echo.

echo [2/5] 安装依赖...
pip install --upgrade pip
pip install bleak>=0.20.0
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

echo [3/5] 使用PyInstaller构建...
pyinstaller --onefile --name "BluetoothSecurityTool" --clean --noconfirm bluetooth_security_app.py
if %errorlevel% neq 0 (
    echo ❌ 构建失败！
    pause
    exit /b 1
)
echo.

echo [4/5] 检查构建产物...
if exist "dist\BluetoothSecurityTool.exe" (
    echo ✅ 构建成功！
    echo.
    echo ============================================
    echo 构建完成！
    echo ============================================
    echo 可执行文件位置：
    echo %cd%\dist\BluetoothSecurityTool.exe
    echo.
    echo 可以将这个文件复制到任何Windows电脑直接使用！
    echo.
) else (
    echo ❌ 未找到构建文件！
    pause
    exit /b 1
)

echo [5/5] 尝试打开文件位置...
explorer dist

echo.
echo 按任意键退出...
pause >nul
