#!/bin/bash

echo "=========================================================="
echo "        Building PDF Document Explorer for macOS"
echo "=========================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install PyInstaller if not already installed
echo "📦 Installing PyInstaller..."
python3 -m pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "❌ Failed to install PyInstaller"
    exit 1
fi

echo "✅ PyInstaller installed"
echo ""

# Build the macOS application
echo "🔨 Building macOS application (Ultra-Compatible: 10.9+ and Intel Macs)..."
python3 -m PyInstaller --noconfirm pdf_explorer.spec

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
        
        # Sign the app
        codesign --force --deep --sign "$SIGNING_IDENTITY" "dist/PDF Document Explorer.app"
        
        if [ $? -eq 0 ]; then
            echo "✅ Application signed successfully!"
            
            # Verify the signature
            codesign --verify --verbose "dist/PDF Document Explorer.app"
            if [ $? -eq 0 ]; then
                echo "✅ Signature verification passed!"
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
echo "🔇 No console window will appear when double-clicked"
echo "🖥️  Ultra-Compatible with macOS 10.9+ (Mavericks) and Intel Macs"
echo "🐍 Supports Python 2.6+ and Python 3.x - maximum compatibility"
echo ""
echo "🎉 You can now distribute this .app bundle!"
echo ""
echo "⚠️  IMPORTANT: If users see a security warning, tell them to:"
echo "   1. Right-click the app → Open"
echo "   2. Click 'Open' in the security dialog"
echo "   3. The app will then work normally"
echo ""

# Make the script executable
chmod +x "$0"
