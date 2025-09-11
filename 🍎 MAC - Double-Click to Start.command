#!/bin/bash

# PDF Document Explorer - Double-Click Starter for macOS
# This .command file can be double-clicked in Finder

echo ""
echo "=========================================================="
echo "        PDF Document Explorer - Starting Server"
echo "=========================================================="
echo ""

# Change to the directory where this script is located
cd "$(dirname "$0")"

# Function to install Python on macOS
install_python_mac() {
    # First try to install Homebrew if it's not installed
    if ! command -v brew &> /dev/null; then
        echo "🍺 Installing Homebrew first..."
        echo "   (Package manager for macOS - this enables automatic Python installation)"
        echo ""
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for the current session
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            # Apple Silicon Mac
            export PATH="/opt/homebrew/bin:$PATH"
        elif [[ -f "/usr/local/bin/brew" ]]; then
            # Intel Mac
            export PATH="/usr/local/bin:$PATH"
        fi
    fi
    
    if command -v brew &> /dev/null; then
        echo "🐍 Installing Python 3 with Homebrew..."
        brew install python
        echo ""
        echo "✅ Python 3 installation completed!"
        echo ""
        
        # Update Python command
        if command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        elif command -v python &> /dev/null; then
            PYTHON_CMD="python"
        else
            echo "❌ Python installation failed. Please install manually:"
            echo "   Download from: https://www.python.org/downloads/"
            echo ""
            read -p "Press Enter to exit..."
            exit 1
        fi
    else
        echo "❌ Could not install Homebrew. Installing Python manually..."
        echo ""
        echo "📥 Please install Python 3 manually:"
        echo "   1. Go to: https://www.python.org/downloads/"
        echo "   2. Download Python 3.11 or later"
        echo "   3. Run the installer"
        echo "   4. Run this script again"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
}

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    if python -c "import sys; exit(0 if sys.version_info.major == 3 else 1)" 2>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Python 3 is required, but only Python 2 was found."
        echo ""
        echo "📥 Installing Python 3 automatically..."
        install_python_mac
    fi
else
    echo "❌ Python is not installed on this Mac."
    echo ""
    echo "📥 Installing Python 3 automatically..."
    echo "   This may take a few minutes. Please wait..."
    echo ""
    install_python_mac
fi

# Check if required files exist
if [ ! -f "web/index.html" ]; then
    echo "❌ Cannot find required files."
    echo ""
    echo "This file must be run from the project folder containing:"
    echo "   - web/index.html"
    echo "   - data/car_references.json"
    echo ""
    echo "Current location: $(pwd)"
    echo ""
    echo "Please ensure the project structure is correct and try again."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python found: $PYTHON_CMD"
echo "✅ Required files found"
echo ""

# Find available port
PORT=8000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT+1))
done

echo "🚀 Starting web server on port $PORT..."
echo ""
echo "🌐 Your web browser will open automatically!"
echo "📱 App URL: http://localhost:$PORT/web/"
echo ""
echo "⏸️  To stop the server: Close this window or press Ctrl+C"
echo ""
echo "=========================================================="

# Start server in background
$PYTHON_CMD -m http.server $PORT &
SERVER_PID=$!

# Wait a moment for server to start
sleep 3

# Open browser
echo ""
echo "✅ Server is running! Opening browser..."
open "http://localhost:$PORT/web/"

echo ""
echo "🎉 PDF Document Explorer is now running!"
echo "   If browser didn't open, go to: http://localhost:$PORT/web/"
echo ""
echo "Press any key to stop the server..."

# Wait for user input
read -n 1 -s

# Stop the server
kill $SERVER_PID 2>/dev/null
echo ""
echo "🛑 Server stopped. Thank you for using PDF Document Explorer!"
echo ""
