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
echo 🔨 Building Windows executable...
%PYTHON_CMD% -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "PDF Document Explorer" ^
    --add-data "web;web" ^
    --add-data "data;data" ^
    --hidden-import tkinter ^
    --hidden-import http.server ^
    --hidden-import webbrowser ^
    --hidden-import threading ^
    --hidden-import socket ^
    --hidden-import signal ^
    --hidden-import platform ^
    pdf_explorer_app.py

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 📁 The executable is located in: dist\PDF Document Explorer.exe
echo.
echo 🎉 You can now distribute this single .exe file!
echo    Users just need to double-click it to run the PDF Explorer.
echo.
pause
