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
echo "🔨 Building macOS application (No Console Version)..."
python3 -m PyInstaller --noconfirm pdf_explorer.spec

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "✅ Build completed successfully!"
echo "📁 The application is located in: dist/PDF Document Explorer.app"
echo "🔇 No console window will appear when double-clicked"
echo ""
echo "🎉 You can now distribute this .app bundle!"
echo "   Users just need to double-click it to run the PDF Explorer."
echo ""

# Make the script executable
chmod +x "$0"
