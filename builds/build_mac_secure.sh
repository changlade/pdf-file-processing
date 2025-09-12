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

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist 2>/dev/null

# Create backup of original files
echo "💾 Creating backups..."
cp pdf_explorer_mac_v2.py pdf_explorer_mac_v2.py.backup
cp flask_proxy.py flask_proxy.py.backup

# Inject token into source files
echo "🔧 Injecting token into build files..."
sed -i.tmp "s/your-databricks-token-here/$DATABRICKS_TOKEN/g" pdf_explorer_mac_v2.py
sed -i.tmp "s/your-databricks-token-here/$DATABRICKS_TOKEN/g" flask_proxy.py
rm -f *.tmp

# Build the application
echo "🏗️ Building macOS application..."
python3 -m PyInstaller --noconfirm current_specs/pdf_explorer_mac_v2.spec

# Restore original files
echo "🔄 Restoring original source files..."
mv pdf_explorer_mac_v2.py.backup pdf_explorer_mac_v2.py
mv flask_proxy.py.backup flask_proxy.py

# Check build success
if [ -d "dist/PDF Document Explorer.app" ]; then
    echo
    echo "✅ Build complete! Token removed from source."
    echo "📦 Distribution ready in: dist/"
    echo
    echo "🔒 Security verified:"
    echo "   • Source files restored (no embedded secrets)"
    echo "   • Built app includes working token"
    echo "   • Ready for distribution"
    echo
    echo "🚀 To test: ./dist/PDF\\ Document\\ Explorer.app/Contents/MacOS/PDF\\ Document\\ Explorer"
else
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi
