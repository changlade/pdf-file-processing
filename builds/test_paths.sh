#!/bin/bash

echo "🔍 Testing Build Paths for All Platforms"
echo "========================================"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

echo "📍 Current directory: $(pwd)"
echo ""

echo "🔍 Checking required files exist:"
echo ""

# Check Python files
if [ -f "pdf_explorer_mac_v2.py" ]; then
    echo "✅ pdf_explorer_mac_v2.py - Found"
else
    echo "❌ pdf_explorer_mac_v2.py - Missing"
fi

if [ -f "pdf_explorer_windows_v2.py" ]; then
    echo "✅ pdf_explorer_windows_v2.py - Found"
else
    echo "❌ pdf_explorer_windows_v2.py - Missing"
fi

if [ -f "flask_proxy.py" ]; then
    echo "✅ flask_proxy.py - Found"
else
    echo "❌ flask_proxy.py - Missing"
fi

echo ""

# Check spec files
echo "🔍 Checking spec files:"
echo ""

if [ -f "current_specs/pdf_explorer_mac_v2.spec" ]; then
    echo "✅ current_specs/pdf_explorer_mac_v2.spec - Found"
else
    echo "❌ current_specs/pdf_explorer_mac_v2.spec - Missing"
fi

if [ -f "current_specs/pdf_explorer_mac_intel.spec" ]; then
    echo "✅ current_specs/pdf_explorer_mac_intel.spec - Found"
else
    echo "❌ current_specs/pdf_explorer_mac_intel.spec - Missing"
fi

if [ -f "current_specs/pdf_explorer_windows_v2.spec" ]; then
    echo "✅ current_specs/pdf_explorer_windows_v2.spec - Found"
else
    echo "❌ current_specs/pdf_explorer_windows_v2.spec - Missing"
fi

echo ""

# Check data directories
echo "🔍 Checking data directories:"
echo ""

if [ -d "web" ] && [ -f "web/index.html" ]; then
    echo "✅ web/ directory - Found with index.html"
else
    echo "❌ web/ directory or index.html - Missing"
fi

if [ -d "data" ] && [ -f "data/pdf_content.json" ]; then
    echo "✅ data/ directory - Found with pdf_content.json"
else
    echo "❌ data/ directory or pdf_content.json - Missing"
fi

echo ""

# Check build scripts
echo "🔍 Checking build scripts:"
echo ""

if [ -f "builds/build_mac_v2.sh" ]; then
    echo "✅ builds/build_mac_v2.sh - Found"
else
    echo "❌ builds/build_mac_v2.sh - Missing"
fi

if [ -f "builds/build_mac_intel.sh" ]; then
    echo "✅ builds/build_mac_intel.sh - Found"
else
    echo "❌ builds/build_mac_intel.sh - Missing"
fi

if [ -f "builds/build_all_mac.sh" ]; then
    echo "✅ builds/build_all_mac.sh - Found"
else
    echo "❌ builds/build_all_mac.sh - Missing"
fi

if [ -f "builds/build_windows_v2.bat" ]; then
    echo "✅ builds/build_windows_v2.bat - Found"
else
    echo "❌ builds/build_windows_v2.bat - Missing"
fi

echo ""
echo "🎯 Path validation complete!"
echo ""
echo "📝 Build script paths in spec files:"
echo "   • Mac ARM64: current_specs/pdf_explorer_mac_v2.spec"
echo "   • Mac Intel: current_specs/pdf_explorer_mac_intel.spec"  
echo "   • Windows: current_specs/pdf_explorer_windows_v2.spec"
echo ""
echo "📝 All spec files reference:"
echo "   • Python files: ../pdf_explorer_*.py"
echo "   • Web assets: ../web -> web"
echo "   • Data files: ../data -> data"
echo ""

chmod +x "$0"
