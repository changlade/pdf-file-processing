#!/bin/bash

# PDF Document Explorer - Auto-Installing Startup Script
# Works on macOS and Linux - automatically installs Python if needed

echo "🚀 Starting PDF Document Explorer..."
echo ""

# Function to install Python on macOS
install_python_mac() {
    echo "🍎 macOS detected - Installing Python automatically..."
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "📦 Using Homebrew to install Python..."
        brew install python3
        return $?
    else
        echo "📦 Installing Homebrew first, then Python..."
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for this session
        if [[ -f /opt/homebrew/bin/brew ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [[ -f /usr/local/bin/brew ]]; then
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        
        # Install Python
        brew install python3
        return $?
    fi
}

# Function to install Python on Linux
install_python_linux() {
    echo "🐧 Linux detected - Installing Python automatically..."
    
    # Detect package manager and install Python
    if command -v apt &> /dev/null; then
        echo "📦 Using apt to install Python..."
        sudo apt update && sudo apt install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        echo "📦 Using yum to install Python..."
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        echo "📦 Using dnf to install Python..."
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        echo "📦 Using pacman to install Python..."
        sudo pacman -S python python-pip
    elif command -v zypper &> /dev/null; then
        echo "📦 Using zypper to install Python..."
        sudo zypper install python3 python3-pip
    else
        echo "❌ Could not detect package manager. Please install Python manually:"
        echo "   Visit: https://www.python.org/downloads/"
        return 1
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
        echo "⚠️  Found Python 2, but need Python 3. Installing Python 3..."
        PYTHON_CMD=""
    fi
else
    PYTHON_CMD=""
fi

# Install Python if not found or wrong version
if [[ -z "$PYTHON_CMD" ]]; then
    echo "🔧 Python 3 not found. Installing automatically..."
    
    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        install_python_mac
        if [[ $? -eq 0 ]]; then
            PYTHON_CMD="python3"
            echo "✅ Python installed successfully!"
        else
            echo "❌ Failed to install Python automatically."
            echo "📥 Please install manually from: https://www.python.org/downloads/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        install_python_linux
        if [[ $? -eq 0 ]]; then
            PYTHON_CMD="python3"
            echo "✅ Python installed successfully!"
        else
            echo "❌ Failed to install Python automatically."
            echo "📥 Please install manually using your package manager or from: https://www.python.org/downloads/"
            exit 1
        fi
    else
        echo "❌ Unsupported operating system: $OSTYPE"
        echo "📥 Please install Python manually from: https://www.python.org/downloads/"
        exit 1
    fi
fi

# Check if we're in the right directory
if [ ! -f "web/index.html" ]; then
    echo "❌ Please run this script from the pdf-file-processing directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Find available port
PORT=8000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT+1))
done

echo "✅ Starting web server on port $PORT"
echo "📱 Open your browser and go to: http://localhost:$PORT/web/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try to open browser automatically
sleep 2 &
if command -v open &> /dev/null; then
    # macOS
    (sleep 3 && open "http://localhost:$PORT/web/") &
elif command -v xdg-open &> /dev/null; then
    # Linux
    (sleep 3 && xdg-open "http://localhost:$PORT/web/") &
fi

# Start the server
$PYTHON_CMD -m http.server $PORT
