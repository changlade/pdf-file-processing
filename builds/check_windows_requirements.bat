@echo off
echo 🔍 Windows Requirements Check
echo.

echo 🐍 Python version:
python --version
echo.

echo 📦 Checking required packages...
echo.

echo Checking Flask...
python -c "import flask; print('✅ Flask version:', flask.__version__)" 2>nul || echo "❌ Flask not found - run: pip install flask"

echo Checking Flask-CORS...
python -c "import flask_cors; print('✅ Flask-CORS installed')" 2>nul || echo "❌ Flask-CORS not found - run: pip install flask-cors"

echo Checking Requests...
python -c "import requests; print('✅ Requests version:', requests.__version__)" 2>nul || echo "❌ Requests not found - run: pip install requests"

echo Checking PyInstaller...
python -c "import PyInstaller; print('✅ PyInstaller version:', PyInstaller.__version__)" 2>nul || echo "❌ PyInstaller not found - run: pip install pyinstaller"

echo.
echo 🔧 To install all requirements:
echo pip install flask flask-cors requests pyinstaller

echo.
echo 📁 Checking project structure...
cd /d "%~dp0\.."
echo Current directory: %CD%
echo.

if exist "pdf_explorer_windows_v2.py" (echo ✅ Main app file found) else (echo ❌ pdf_explorer_windows_v2.py missing)
if exist "flask_proxy.py" (echo ✅ Proxy file found) else (echo ❌ flask_proxy.py missing)
if exist "web" (echo ✅ Web directory found) else (echo ❌ web directory missing)
if exist "data" (echo ✅ Data directory found) else (echo ❌ data directory missing)
if exist "current_specs" (echo ✅ Specs directory found) else (echo ❌ current_specs directory missing)
if exist "current_specs\pdf_explorer_windows_v2.spec" (echo ✅ Windows spec file found) else (echo ❌ Windows spec file missing)

echo.
pause
