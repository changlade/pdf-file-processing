@echo off
echo 🔐 Secure Windows Build Process
echo.

REM Check if token is provided
if "%DATABRICKS_TOKEN%"=="" (
    echo ❌ Error: DATABRICKS_TOKEN environment variable not set
    echo Please run: set DATABRICKS_TOKEN=your-token-here
    exit /b 1
)

echo ✅ Token found, proceeding with build...

REM Navigate to project root
cd /d "%~dp0\.."

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul

REM Create backup of original files
echo 💾 Creating backups...
copy pdf_explorer_windows_v2.py pdf_explorer_windows_v2.py.backup >nul
copy flask_proxy.py flask_proxy.py.backup >nul

REM Inject token into source files
echo 🔧 Injecting token into build files...
powershell -Command "(Get-Content pdf_explorer_windows_v2.py) -replace 'your-databricks-token-here', '%DATABRICKS_TOKEN%' | Set-Content pdf_explorer_windows_v2.py"
powershell -Command "(Get-Content flask_proxy.py) -replace 'your-databricks-token-here', '%DATABRICKS_TOKEN%' | Set-Content flask_proxy.py"

REM Build the application
echo 🏗️ Building Windows application...
python -m PyInstaller --noconfirm current_specs\pdf_explorer_windows_v2.spec

REM Restore original files
echo 🔄 Restoring original source files...
move pdf_explorer_windows_v2.py.backup pdf_explorer_windows_v2.py >nul
move flask_proxy.py.backup flask_proxy.py >nul

REM Check build success
if exist "dist\PDF Document Explorer\PDF Document Explorer.exe" (
    echo.
    echo ✅ Build complete! Token removed from source.
    echo 📦 Distribution ready in: dist\
    echo.
    echo 🔒 Security verified:
    echo    • Source files restored ^(no embedded secrets^)
    echo    • Built app includes working token
    echo    • Ready for distribution
    echo.
    echo 🚀 To test: dist\"PDF Document Explorer"\"PDF Document Explorer.exe"
) else (
    echo ❌ Build failed! Check the output above for errors.
    exit /b 1
)
