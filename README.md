# PDF Document Explorer with Semantic Search

A powerful PDF viewer with AI-powered semantic search capabilities, built with Python, Flask, and JavaScript.

## 🚀 Features

- **📄 PDF Viewing**: Full-featured PDF viewer with page navigation
- **🔍 CAR Reference Search**: Search for specific document references
- **🧠 Semantic Search**: AI-powered search using Databricks Vector Search
- **🎯 Smart Navigation**: Click on search results to jump to specific PDF pages
- **📱 Responsive UI**: Modern, clean interface with search mode toggle

## 📁 Project Structure

```
pdf-file-processing/
├── 📄 README.md                     # This file
├── 🐍 pdf_explorer_mac_v2.py        # macOS application (current)
├── 🐍 pdf_explorer_windows_v2.py    # Windows application (current)
├── 🐍 flask_proxy.py               # Flask proxy server for semantic search
├── 📂 builds/                       # Build scripts and configurations
│   ├── 🔨 build_mac_v2.sh          # macOS build script
│   └── 🔨 build_windows_v2.bat     # Windows build script
├── 📂 current_specs/               # PyInstaller specifications
│   ├── pdf_explorer_mac_v2.spec    # macOS ARM64 spec
│   ├── pdf_explorer_mac_intel.spec # macOS Intel x86_64 spec
│   └── pdf_explorer_windows_v2.spec # Windows spec
├── 📂 web/                         # Frontend files
│   ├── index.html                  # Main application UI
│   └── jugement.pdf               # Sample PDF file
├── 📂 data/                        # Data files
│   ├── car_references.json        # CAR reference database
│   ├── pdf_content.json          # PDF content blocks
│   └── jugement.pdf               # PDF document
├── 📂 src/                         # Source utilities
│   ├── extract_car_references.py  # CAR reference extractor
│   ├── inspect_json.py           # JSON inspector utility
│   ├── pdf_processor.py          # PDF processing utilities
│   └── requirements.txt          # Python dependencies
├── 📂 archive/                     # Archived old files
│   ├── deprecated/               # Old Python files
│   ├── old_specs/               # Old PyInstaller specs
│   ├── old_scripts/             # Old build scripts
│   └── old_builds/              # Old build artifacts
├── 📂 dist/                        # Built applications (generated)
├── 📂 build/                       # Build cache (generated)
└── 📂 venv/                        # Python virtual environment
```

## 🛠️ Building Applications

### 🍎 macOS

**For Apple Silicon (M1/M2/M3):**
```bash
cd builds
./build_mac_v2.sh
```

**For Intel Macs:**
```bash
cd builds
# First, update the spec to use intel spec
source ../venv/bin/activate
python3 -m PyInstaller --noconfirm ../current_specs/pdf_explorer_mac_intel.spec
```

### 🪟 Windows

```cmd
cd builds
build_windows_v2.bat
```

## 🧠 Semantic Search Setup

The semantic search feature requires:

1. **Internet Connection**: To access Databricks Vector Search API
2. **Flask Proxy**: Automatically started by the applications
3. **API Configuration**: Databricks token required (see [CONFIGURATION.md](CONFIGURATION.md))

### Quick Setup
```bash
export DATABRICKS_TOKEN="your-actual-databricks-token"
```

See [CONFIGURATION.md](CONFIGURATION.md) for detailed setup instructions.

### Manual Proxy Server (Development)

To run the proxy server separately:

```bash
source venv/bin/activate
python3 flask_proxy.py
```

The proxy will be available at: `http://127.0.0.1:8002`

## 📋 Dependencies

- **Python 3.8+**
- **Flask & Flask-CORS** (for semantic search proxy)
- **Requests** (for API calls)
- **PyInstaller** (for building executables)

## 🎯 Usage

1. **Launch the Application**: Double-click the built executable
2. **Choose Search Mode**: Toggle between "CAR" and "Semantic" search
3. **Search**: Enter your query and press Enter or click Search
4. **Navigate**: Click on results to jump to relevant PDF pages

### CAR Search
- Search for specific document references (e.g., "CAR/123")
- Results show reference counts and locations

### Semantic Search
- AI-powered contextual search (e.g., "war crimes evidence")
- Results show similarity scores and content summaries
- Powered by Databricks Vector Search

## 🔧 Development

### Running Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install flask flask-cors requests

# Start the web server (manual)
cd web
python3 -m http.server 8000

# Start the proxy server (separate terminal)
python3 flask_proxy.py

# Open browser
open http://localhost:8000
```

### Architecture

- **Frontend**: HTML/CSS/JavaScript with PDF.js
- **Backend**: Python Flask proxy server
- **PDF Processing**: Custom JSON-based content extraction
- **Search**: Databricks Vector Search API integration
- **Build**: PyInstaller for executable generation

## 📝 Notes

- **macOS Security**: Apps may show security warnings. Right-click → Open to approve
- **Windows Defender**: May flag the executable. Add to exclusions if needed
- **Network**: Semantic search requires internet access to Databricks

## 🗂️ Archive

Old files and deprecated versions are stored in the `archive/` folder:
- `archive/deprecated/` - Old Python application files
- `archive/old_specs/` - Previous PyInstaller specifications
- `archive/old_scripts/` - Legacy build scripts
- `archive/old_builds/` - Previous build artifacts

---

**Version**: 2.0.0 with Semantic Search  
**Last Updated**: September 2025
