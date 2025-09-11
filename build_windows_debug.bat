@echo off
echo ==========================================================
echo       Building PDF Document Explorer DEBUG for Windows
echo ==========================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is not installed. Please install Python first.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python found: %PYTHON_CMD%
echo.

REM Install PyInstaller if not already installed
echo 📦 Installing PyInstaller...
%PYTHON_CMD% -m pip install pyinstaller
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller installed
echo.

REM Build the Windows executable
echo 🔨 Building Windows DEBUG executable...
%PYTHON_CMD% -m PyInstaller --noconfirm pdf_explorer_windows_debug.spec

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✅ DEBUG Build completed successfully!
echo 📁 The executable is located in: dist\PDF Document Explorer Debug\PDF Document Explorer Debug.exe
echo 🔍 Console will show debugging information
echo.
echo 🎯 Test this version first to see what's happening!
echo.
pause
