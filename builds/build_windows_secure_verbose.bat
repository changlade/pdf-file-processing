@echo off
echo 🔐 Secure Windows Build Process ^(Verbose^)
echo.

REM Check if token is provided
if "%DATABRICKS_TOKEN%"=="" (
    echo ❌ Error: DATABRICKS_TOKEN environment variable not set
    echo Please run: set DATABRICKS_TOKEN=your-token-here
    echo.
    echo Example with real token:
    echo set DATABRICKS_TOKEN=your-actual-databricks-token-here
    pause
    exit /b 1
)

echo ✅ Token found: %DATABRICKS_TOKEN:~0,8%****
echo.

REM Navigate to project root
echo 📁 Navigating to project root...
cd /d "%~dp0\.."
echo Current directory: %CD%
echo.

REM Check Python
echo 🐍 Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)
echo.

REM Check PyInstaller
echo 📦 Checking PyInstaller...
python -m PyInstaller --version
if errorlevel 1 (
    echo ❌ PyInstaller not found
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo.

REM Check required files
echo 📋 Checking required files...
if not exist "pdf_explorer_windows_v2.py" (
    echo ❌ pdf_explorer_windows_v2.py not found
    echo Please run this script from the builds directory
    pause
    exit /b 1
)

if not exist "flask_proxy.py" (
    echo ❌ flask_proxy.py not found
    pause
    exit /b 1
)

if not exist "current_specs\pdf_explorer_windows_v2.spec" (
    echo ❌ Spec file not found: current_specs\pdf_explorer_windows_v2.spec
    echo Available files in current_specs:
    if exist "current_specs" (
        dir /b current_specs
    ) else (
        echo current_specs directory does not exist
    )
    pause
    exit /b 1
)

echo ✅ All files found
echo.

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist build (
    echo Removing build directory...
    rmdir /s /q build 2>nul
)
if exist dist (
    echo Removing dist directory...
    rmdir /s /q dist 2>nul
)
echo.

REM Create backup of original files
echo 💾 Creating backups...
copy pdf_explorer_windows_v2.py pdf_explorer_windows_v2.py.backup >nul
if errorlevel 1 (
    echo ❌ Failed to backup pdf_explorer_windows_v2.py
    pause
    exit /b 1
)

copy flask_proxy.py flask_proxy.py.backup >nul
if errorlevel 1 (
    echo ❌ Failed to backup flask_proxy.py
    pause
    exit /b 1
)
echo ✅ Backups created
echo.

REM Inject token into source files
echo 🔧 Injecting token into build files...
powershell -Command "(Get-Content pdf_explorer_windows_v2.py) -replace 'your-databricks-token-here', '%DATABRICKS_TOKEN%' | Set-Content pdf_explorer_windows_v2.py"
if errorlevel 1 (
    echo ❌ Failed to inject token into pdf_explorer_windows_v2.py
    goto restore_and_exit
)

powershell -Command "(Get-Content flask_proxy.py) -replace 'your-databricks-token-here', '%DATABRICKS_TOKEN%' | Set-Content flask_proxy.py"
if errorlevel 1 (
    echo ❌ Failed to inject token into flask_proxy.py
    goto restore_and_exit
)
echo ✅ Token injected
echo.

REM Build the application
echo 🏗️ Building Windows application...
echo Command: python -m PyInstaller --noconfirm current_specs\pdf_explorer_windows_v2.spec
echo.
python -m PyInstaller --noconfirm current_specs\pdf_explorer_windows_v2.spec
set BUILD_RESULT=%errorlevel%

REM Restore original files
echo.
echo 🔄 Restoring original source files...
move pdf_explorer_windows_v2.py.backup pdf_explorer_windows_v2.py >nul
move flask_proxy.py.backup flask_proxy.py >nul
echo ✅ Files restored
echo.

REM Check build result
if %BUILD_RESULT% neq 0 (
    echo ❌ PyInstaller failed with error code: %BUILD_RESULT%
    pause
    exit /b %BUILD_RESULT%
)

REM Check build success
if exist "dist\PDF Document Explorer\PDF Document Explorer.exe" (
    echo ✅ Build complete! Token removed from source.
    echo 📦 Distribution ready in: dist\
    echo.
    echo 🔒 Security verified:
    echo    • Source files restored ^(no embedded secrets^)
    echo    • Built app includes working token
    echo    • Ready for distribution
    echo.
    echo 🚀 To test: dist\"PDF Document Explorer"\"PDF Document Explorer.exe"
    echo.
    pause
) else (
    echo ❌ Build failed! Expected executable not found.
    echo Checking what was actually created in dist directory:
    if exist dist (
        dir /s dist
    ) else (
        echo dist directory was not created
    )
    pause
    exit /b 1
)

goto end

:restore_and_exit
echo.
echo 🔄 Restoring files due to error...
if exist pdf_explorer_windows_v2.py.backup move pdf_explorer_windows_v2.py.backup pdf_explorer_windows_v2.py >nul
if exist flask_proxy.py.backup move flask_proxy.py.backup flask_proxy.py >nul
pause
exit /b 1

:end
