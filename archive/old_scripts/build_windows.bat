@echo off
echo ==========================================================
echo          Building PDF Document Explorer for Windows
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
echo 🔨 Building Windows executable (Fast Startup Version)...
%PYTHON_CMD% -m PyInstaller --noconfirm pdf_explorer_windows.spec

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📁 The executable is located in: dist\PDF Document Explorer\PDF Document Explorer.exe
echo ⚡ Fast startup (2-3 seconds), reliable server detection, auto cleanup
echo 🔇 Console shows briefly during startup, then auto-hides
echo.
echo 🎉 You can now distribute the entire "PDF Document Explorer" folder!
echo    Users just need to double-click the .exe inside the folder.
echo.
pause
