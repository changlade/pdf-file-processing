#!/bin/bash

echo "=========================================================="
echo "        Building PDF Document Explorer for macOS"
echo "          All Architectures (ARM64 + Intel x86_64)"
echo "           with Semantic Search Support"
echo "=========================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check Python version (need 3.8+)
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 8 ]); then
    echo "❌ Python 3.8+ is required for semantic search features. Found: $python_version"
    exit 1
fi

echo "✅ Python version is compatible: $python_version"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

# Install required packages
echo "📦 Installing required packages..."
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller flask flask-cors requests

if [ $? -ne 0 ]; then
    echo "❌ Failed to install required packages"
    exit 1
fi

echo "✅ Required packages installed"
echo ""

# Detect current architecture
CURRENT_ARCH=$(uname -m)
echo "🔍 Current architecture: $CURRENT_ARCH"
echo ""

# Build for current architecture first
if [ "$CURRENT_ARCH" = "arm64" ]; then
    echo "🔨 Building for Apple Silicon (ARM64)..."
    python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_v2.spec
    ARM_BUILD_SUCCESS=$?
    
    echo ""
    echo "🔨 Building for Intel (x86_64)..."
    echo "⚠️  Note: Cross-compilation may have limitations"
    python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_intel.spec
    INTEL_BUILD_SUCCESS=$?
else
    echo "🔨 Building for Intel (x86_64)..."
    python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_intel.spec
    INTEL_BUILD_SUCCESS=$?
    
    echo ""
    echo "🔨 Building for Apple Silicon (ARM64)..."
    echo "⚠️  Note: Cross-compilation may have limitations"
    python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_v2.spec
    ARM_BUILD_SUCCESS=$?
fi

echo ""
echo "📊 Build Results:"

if [ $ARM_BUILD_SUCCESS -eq 0 ]; then
    echo "✅ Apple Silicon (ARM64) build: SUCCESS"
    echo "   📁 Location: dist/PDF Document Explorer.app"
else
    echo "❌ Apple Silicon (ARM64) build: FAILED"
fi

if [ $INTEL_BUILD_SUCCESS -eq 0 ]; then
    echo "✅ Intel (x86_64) build: SUCCESS"
    echo "   📁 Location: dist/PDF Document Explorer Intel.app"
else
    echo "❌ Intel (x86_64) build: FAILED"
fi

echo ""

# Code signing for successful builds
if command -v codesign &> /dev/null; then
    SIGNING_IDENTITY=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -1 | cut -d'"' -f2)
    
    if [ ! -z "$SIGNING_IDENTITY" ]; then
        echo "🔐 Code signing applications..."
        echo "📝 Found signing identity: $SIGNING_IDENTITY"
        
        if [ $ARM_BUILD_SUCCESS -eq 0 ] && [ -d "dist/PDF Document Explorer.app" ]; then
            echo "🔏 Signing Apple Silicon version..."
            codesign --force --deep --options runtime --sign "$SIGNING_IDENTITY" "dist/PDF Document Explorer.app"
        fi
        
        if [ $INTEL_BUILD_SUCCESS -eq 0 ] && [ -d "dist/PDF Document Explorer Intel.app" ]; then
            echo "🔏 Signing Intel version..."
            codesign --force --deep --options runtime --sign "$SIGNING_IDENTITY" "dist/PDF Document Explorer Intel.app"
        fi
        
        echo "✅ Code signing completed!"
    else
        echo "⚠️  No Developer ID found - apps will show security warnings"
    fi
else
    echo "⚠️  codesign not available - apps will show security warnings"
fi

echo ""
echo "🎯 Architecture Details:"

if [ -f "dist/PDF Document Explorer.app/Contents/MacOS/PDF Document Explorer" ]; then
    echo "🍎 Apple Silicon version:"
    file "dist/PDF Document Explorer.app/Contents/MacOS/PDF Document Explorer"
fi

if [ -f "dist/PDF Document Explorer Intel.app/Contents/MacOS/PDF Document Explorer" ]; then
    echo "💻 Intel version:"
    file "dist/PDF Document Explorer Intel.app/Contents/MacOS/PDF Document Explorer"
fi

echo ""
echo "🎉 Build process completed!"
echo ""
echo "📋 Distribution Guide:"
echo "• Apple Silicon Macs (M1/M2/M3): Use 'PDF Document Explorer.app'"
echo "• Intel Macs: Use 'PDF Document Explorer Intel.app'"
echo "• Both versions include AI-powered semantic search"
echo ""
echo "⚠️  Security Note: If users see warnings, tell them to:"
echo "   1. Right-click the app → Open"
echo "   2. Click 'Open' in the security dialog"
echo ""

# Make the script executable
chmod +x "$0"
