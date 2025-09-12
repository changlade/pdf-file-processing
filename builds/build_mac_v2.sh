#!/bin/bash

echo "=========================================================="
echo "    Building PDF Document Explorer v2 for macOS"
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

# Build the macOS application
echo "🔨 Building macOS application with Semantic Search..."
echo "🎯 Target: Current Architecture (will run on same architecture)"
python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_v2.spec

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "🔐 Attempting to sign the application..."

# Try to sign the app if developer tools are available
if command -v codesign &> /dev/null; then
    # Check if we have a signing identity
    SIGNING_IDENTITY=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -1 | cut -d'"' -f2)
    
    if [ ! -z "$SIGNING_IDENTITY" ]; then
        echo "📝 Found signing identity: $SIGNING_IDENTITY"
        echo "🔏 Signing application..."
        
        # Sign the app with hardened runtime
        codesign --force --deep --options runtime --sign "$SIGNING_IDENTITY" "dist/PDF Document Explorer.app"
        
        if [ $? -eq 0 ]; then
            echo "✅ Application signed successfully with hardened runtime!"
            
            # Verify the signature
            codesign --verify --verbose "dist/PDF Document Explorer.app"
            if [ $? -eq 0 ]; then
                echo "✅ Signature verification passed!"
                
                # Check if we can notarize
                echo "🍎 Checking for notarization capability..."
                if command -v xcrun &> /dev/null; then
                    echo "📦 Creating notarization-ready package..."
                    ditto -c -k --keepParent "dist/PDF Document Explorer.app" "dist/PDF Document Explorer.zip"
                    echo "✅ Notarization package created: dist/PDF Document Explorer.zip"
                    echo "ℹ️  To notarize: xcrun notarytool submit 'dist/PDF Document Explorer.zip' --keychain-profile 'notarytool-profile' --wait"
                fi
            else
                echo "⚠️  Signature verification failed, but app is signed"
            fi
        else
            echo "⚠️  Code signing failed - app will show security warning"
        fi
    else
        echo "⚠️  No Developer ID found - app will show security warning"
    fi
else
    echo "⚠️  codesign not available - app will show security warning"
fi

echo ""
echo "✅ Build completed successfully!"
echo "📁 The application is located in: dist/PDF Document Explorer.app"
echo "🧠 Features: PDF viewing + AI-powered semantic search"
echo "🍎 Target: macOS 10.15+ (Catalina) with Universal Binary support"
echo "🔧 Architecture: Built for $(uname -m) (current machine architecture)"
echo ""
echo "🎉 You can now distribute this .app bundle!"
echo ""

# Check architecture
if [ -f "dist/PDF Document Explorer.app/Contents/MacOS/PDF Document Explorer" ]; then
    echo "🔍 Architecture check:"
    file "dist/PDF Document Explorer.app/Contents/MacOS/PDF Document Explorer"
    echo ""
fi

echo "⚠️  IMPORTANT: If users see a security warning, tell them to:"
echo "   1. Right-click the app → Open"
echo "   2. Click 'Open' in the security dialog"
echo "   3. The app will then work normally"
echo ""
echo "🌐 Requirements for semantic search:"
echo "   • Internet connection"
echo "   • Access to dbc-0619d7f5-0bda.cloud.databricks.com"
echo ""

# Make the script executable
chmod +x "$0"
