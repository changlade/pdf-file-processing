# 🏗️ Build Configuration Guide

## 📋 Overview

This guide explains how to properly configure secrets for distribution builds without storing them in the source code.

## 🔐 Secret Management for Builds

### ⚠️ Important Security Note
**NEVER commit API tokens to the repository!** This guide shows how to inject secrets at build time only.

## 🛠️ Method 1: Environment Variable at Build Time

### For Windows Builds:
```cmd
# Set the token before building
set DATABRICKS_TOKEN=your-actual-databricks-token-here
cd builds
build_windows_v2.bat
```

### For macOS Builds:
```bash
# Set the token before building
export DATABRICKS_TOKEN=your-actual-databricks-token-here
./builds/build_mac_v2.sh
```

## 🛠️ Method 2: Build Script with Token Injection

Create a secure build script that temporarily modifies the code during build:

### Windows Build Script (`builds/build_windows_secure.bat`):
```cmd
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

REM Create backup of original files
copy pdf_explorer_windows_v2.py pdf_explorer_windows_v2.py.backup

REM Inject token into source file
powershell -Command "(Get-Content pdf_explorer_windows_v2.py) -replace 'your-databricks-token-here', '%DATABRICKS_TOKEN%' | Set-Content pdf_explorer_windows_v2.py"

REM Build the application
python -m PyInstaller --noconfirm current_specs\pdf_explorer_windows_v2.spec

REM Restore original file
move pdf_explorer_windows_v2.py.backup pdf_explorer_windows_v2.py

echo ✅ Build complete! Token removed from source.
echo 📦 Distribution ready in: dist\
```

### macOS Build Script (`builds/build_mac_secure.sh`):
```bash
#!/bin/bash
echo "🔐 Secure macOS Build Process"
echo

# Check if token is provided
if [ -z "$DATABRICKS_TOKEN" ]; then
    echo "❌ Error: DATABRICKS_TOKEN environment variable not set"
    echo "Please run: export DATABRICKS_TOKEN=your-token-here"
    exit 1
fi

echo "✅ Token found, proceeding with build..."

# Navigate to project root
cd "$(dirname "$0")/.."

# Create backup of original files
cp pdf_explorer_mac_v2.py pdf_explorer_mac_v2.py.backup
cp flask_proxy.py flask_proxy.py.backup

# Inject token into source files
sed -i.tmp "s/your-databricks-token-here/$DATABRICKS_TOKEN/g" pdf_explorer_mac_v2.py
sed -i.tmp "s/your-databricks-token-here/$DATABRICKS_TOKEN/g" flask_proxy.py
rm *.tmp

# Build the application
python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_v2.spec

# Restore original files
mv pdf_explorer_mac_v2.py.backup pdf_explorer_mac_v2.py
mv flask_proxy.py.backup flask_proxy.py

echo "✅ Build complete! Token removed from source."
echo "📦 Distribution ready in: dist/"
```

## 🛠️ Method 3: PyInstaller with Runtime Data

Alternatively, create a separate token file that's included only in the build:

### Create `token_config.py` (add to .gitignore):
```python
# This file is created at build time and excluded from git
DATABRICKS_TOKEN = "your-token-will-be-injected-here"
```

### Update main application to import from this file:
```python
try:
    from token_config import DATABRICKS_TOKEN
except ImportError:
    DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN', 'your-databricks-token-here')
```

## 📋 Recommended Workflow

### Step 1: Prepare Build Environment
```bash
# Set your token (replace with actual token)
export DATABRICKS_TOKEN=your-actual-databricks-token-here
```

### Step 2: Run Secure Build
```bash
# For macOS
./builds/build_mac_secure.sh

# For Windows
builds\build_windows_secure.bat
```

### Step 3: Verify
```bash
# Confirm source files are clean (no token embedded)
git status
# Should show no changes
```

### Step 4: Test Distribution
```bash
# Test the built application
./dist/PDF\ Document\ Explorer.app/Contents/MacOS/PDF\ Document\ Explorer
# Semantic search should work with embedded token
```

## 🔒 Security Best Practices

1. **Never commit tokens**: Always use environment variables or build-time injection
2. **Use secure build scripts**: Automatically clean up after build
3. **Verify clean state**: Check `git status` after build
4. **Backup originals**: Always restore source files after build
5. **Test distributions**: Verify semantic search works in built apps

## ⚠️ Important Notes

- The token is only embedded in the **built application**, not in source code
- Source files remain clean and safe to commit
- Built applications work out-of-the-box for end users
- Development still uses environment variables

## 🎯 Quick Reference

**For immediate testing:**
```bash
export DATABRICKS_TOKEN=your-actual-databricks-token-here
./builds/build_mac_v2.sh
```

**For production builds:**
```bash
export DATABRICKS_TOKEN=your-actual-production-token
./builds/build_mac_secure.sh
```
