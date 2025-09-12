@echo off
echo 🧪 Simple Windows Build Test
echo.

REM Navigate to project root
cd /d "%~dp0\.."

echo 📍 Current directory: %CD%
echo.

echo 🔧 Testing basic PyInstaller command...
python -m PyInstaller --version
if errorlevel 1 (
    echo ❌ PyInstaller failed
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo 🏗️ Attempting simple build...
python -m PyInstaller --onedir --name="Test Build" --distpath=test_dist pdf_explorer_windows_v2.py

echo.
if exist "test_dist\Test Build\Test Build.exe" (
    echo ✅ Simple build successful!
    echo 📦 Test executable: test_dist\Test Build\Test Build.exe
    echo.
    echo 🧹 Cleaning up test build...
    rmdir /s /q test_dist 2>nul
    rmdir /s /q build 2>nul
    del "Test Build.spec" 2>nul
) else (
    echo ❌ Simple build failed
)

pause
