@echo off
echo ==========================================================
echo     Building PDF Document Explorer v2 for Windows
echo            with Semantic Search Support
echo ==========================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Check Python version (need 3.8+)
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python version: %python_version%
echo.

REM Navigate to project root
cd /d "%~dp0\.."

REM Install required packages
echo 📦 Installing required packages...
python -m pip install --upgrade pip
python -m pip install pyinstaller flask flask-cors requests

if errorlevel 1 (
    echo ❌ Failed to install required packages
    pause
    exit /b 1
)

echo ✅ Required packages installed
echo.

REM Build the Windows application
echo 🔨 Building Windows application with Semantic Search...
python -m PyInstaller --noconfirm current_specs\pdf_explorer_windows_v2.spec

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📁 The application is located in: dist\PDF Document Explorer\
echo 🧠 Features: PDF viewing + AI-powered semantic search
echo 🪟 Target: Windows 10+ with Python 3.8+ support
echo.
echo 🎉 You can now distribute the "PDF Document Explorer" folder!
echo.
echo ⚠️  IMPORTANT DISTRIBUTION NOTES:
echo    • Distribute the entire "dist\PDF Document Explorer" folder
echo    • Users need internet connection for semantic search
echo    • Windows Defender may show a warning - this is normal for unsigned apps
echo.
echo 🌐 Requirements for semantic search:
echo    • Internet connection
echo    • Access to dbc-0619d7f5-0bda.cloud.databricks.com
echo.
echo 🚀 To test the application:
echo    1. Navigate to: dist\PDF Document Explorer\
echo    2. Double-click: PDF Document Explorer.exe
echo.

pause
