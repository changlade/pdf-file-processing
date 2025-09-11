@echo off
title PDF Document Explorer - Starting...

echo.
echo ==========================================================
echo          PDF Document Explorer - Starting Server
echo ==========================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is not installed on this computer.
        echo.
        echo 📥 Downloading and installing Python automatically...
        echo    This may take a few minutes. Please wait...
        echo.
        
        REM Download Python installer
        powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-installer.exe'}"
        
        if not exist "python-installer.exe" (
            echo ❌ Failed to download Python installer.
            echo.
            echo 📥 Please install Python manually:
            echo    1. Go to: https://www.python.org/downloads/
            echo    2. Download Python 3.x
            echo    3. During installation, check "Add Python to PATH"
            echo    4. Run this file again after installation
            echo.
            pause
            exit /b 1
        )
        
        echo ✅ Python downloaded. Installing...
        echo    (This window may appear to freeze - that's normal)
        echo.
        
        REM Install Python silently
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        
        REM Clean up installer
        del python-installer.exe >nul 2>&1
        
        echo ✅ Python installation completed!
        echo.
        echo 🔄 Restarting script to use newly installed Python...
        echo.
        timeout /t 3 /nobreak >nul
        
        REM Restart this script to pick up the new Python installation
        "%~f0"
        exit /b 0
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

REM Check if we're in the right directory
if not exist "web\index.html" (
    echo ❌ Cannot find required files.
    echo.
    echo This file must be run from the project folder containing:
    echo    - web\index.html
    echo    - data\car_references.json
    echo.
    echo Current location: %CD%
    echo.
    echo Please ensure the project structure is correct and try again.
    pause
    exit /b 1
)

echo ✅ Python found: %PYTHON_CMD%
echo ✅ Required files found
echo.

REM Find available port
set PORT=8000
netstat -an | find "LISTENING" | find ":%PORT%" >nul
if not errorlevel 1 (
    set PORT=8001
    netstat -an | find "LISTENING" | find ":%PORT%" >nul
    if not errorlevel 1 (
        set PORT=8002
    )
)

echo 🚀 Starting web server on port %PORT%...
echo.
echo 🌐 Your web browser will open automatically!
echo 📱 App URL: http://localhost:%PORT%/web/
echo.
echo ⏸️  To stop the server: Close this window or press Ctrl+C
echo.
echo ==========================================================

REM Wait a moment then open browser
timeout /t 3 /nobreak >nul
start "" "http://localhost:%PORT%/web/"

REM Start the server
echo.
echo ✅ Server is running! Browser should open automatically.
echo    If not, open: http://localhost:%PORT%/web/
echo.
%PYTHON_CMD% -m http.server %PORT%

REM This runs when server stops
echo.
echo 🛑 Server stopped.
echo.
pause
