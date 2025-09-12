@echo off
echo 🔍 Windows Build Debug Information
echo.

echo 📍 Current directory: %CD%
echo.

echo 🔧 Environment check:
echo - DATABRICKS_TOKEN: %DATABRICKS_TOKEN%
echo.

echo 🐍 Python check:
python --version 2>nul && echo ✅ Python found || echo ❌ Python not found
echo.

echo 📦 PyInstaller check:
python -m PyInstaller --version 2>nul && echo ✅ PyInstaller found || echo ❌ PyInstaller not found
echo.

echo 📁 Checking required files:
if exist "pdf_explorer_windows_v2.py" (echo ✅ pdf_explorer_windows_v2.py found) else (echo ❌ pdf_explorer_windows_v2.py NOT found)
if exist "flask_proxy.py" (echo ✅ flask_proxy.py found) else (echo ❌ flask_proxy.py NOT found)
if exist "current_specs\pdf_explorer_windows_v2.spec" (echo ✅ spec file found) else (echo ❌ spec file NOT found)
echo.

echo 📂 Directory contents:
dir /b
echo.

echo 📂 current_specs directory:
if exist "current_specs" (
    dir /b current_specs
) else (
    echo ❌ current_specs directory NOT found
)
echo.

if "%DATABRICKS_TOKEN%"=="" (
    echo ⚠️  DATABRICKS_TOKEN not set. To set it:
    echo    set DATABRICKS_TOKEN=your-token-here
    echo.
) else (
    echo ✅ DATABRICKS_TOKEN is set ^(length: %DATABRICKS_TOKEN:~0,4%****^)
    echo.
    echo 🔧 Would you like to proceed with the build? ^(Y/N^)
    set /p proceed=
    if /i "%proceed%"=="Y" (
        echo.
        echo 🚀 Starting build process...
        call build_windows_secure.bat
    )
)

pause
