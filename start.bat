@echo off
REM PDF Document Explorer - Auto-Installing Startup Script for Windows

echo 🚀 Starting PDF Document Explorer...
echo.

REM Start by checking Python
call :check_python

REM Function to install Python automatically
:install_python
echo 🪟 Windows detected - Installing Python automatically...
echo 📦 Downloading Python installer...

REM Create temp directory
if not exist "%TEMP%\pdf-explorer-setup" mkdir "%TEMP%\pdf-explorer-setup"
cd /d "%TEMP%\pdf-explorer-setup"

REM Download Python installer (latest 3.11 for compatibility)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'}"

if not exist "python-installer.exe" (
    echo ❌ Failed to download Python installer
    echo 📥 Please install Python manually from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo 🔧 Installing Python... (this may take a few minutes)
echo    ⚠️  Please wait and don't close this window
echo    ✅ The installer will add Python to your PATH automatically

REM Install Python silently with PATH added
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait for installation to complete
timeout /t 10 /nobreak >nul

REM Clean up
del python-installer.exe

REM Refresh environment variables by restarting script
echo ✅ Python installation completed! Restarting script...
echo.
cd /d "%~dp0"
call "%~f0"
exit /b 0

:check_python
REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        REM Check if we already tried installing
        if "%PYTHON_INSTALL_ATTEMPTED%"=="1" (
            echo ❌ Python installation failed or Python not found in PATH
            echo 📥 Please install Python manually from: https://www.python.org/downloads/
            echo    Make sure to check "Add Python to PATH" during installation
            pause
            exit /b 1
        )
        
        REM Try to install Python
        set PYTHON_INSTALL_ATTEMPTED=1
        goto install_python
    ) else (
        set PYTHON_CMD=py
    )
) else (
    REM Check if it's Python 3
    python -c "import sys; exit(0 if sys.version_info.major == 3 else 1)" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Found Python 2, but need Python 3. Installing Python 3...
        if "%PYTHON_INSTALL_ATTEMPTED%"=="1" (
            echo ❌ Python 3 installation failed
            echo 📥 Please install Python 3 manually from: https://www.python.org/downloads/
            pause
            exit /b 1
        )
        set PYTHON_INSTALL_ATTEMPTED=1
        goto install_python
    ) else (
        set PYTHON_CMD=python
    )
)

goto continue_setup

:continue_setup

REM Check if we're in the right directory
if not exist "web\index.html" (
    echo ❌ Please run this script from the pdf-file-processing directory
    echo    Current directory: %CD%
    pause
    exit /b 1
)

REM Use port 8000 (simple approach for Windows)
set PORT=8000

echo ✅ Starting web server on port %PORT%
echo 📱 Open your browser and go to: http://localhost:%PORT%/web/
echo.
echo Press Ctrl+C to stop the server
echo.

REM Open browser after a short delay
timeout /t 3 /nobreak >nul
start "" "http://localhost:%PORT%/web/"

REM Start the server
%PYTHON_CMD% -m http.server %PORT%
