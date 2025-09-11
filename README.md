# PDF Document Explorer

A web application for exploring PDF documents and searching for CAR (Central African Republic) references with interactive highlighting and navigation.

## 🚀 Quick Start

To run the web application on your laptop:

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.7+ (only needed if you want to regenerate data)

### Running the Web Application

1. **Download or clone this project** to your laptop

2. **Open a terminal/command prompt** and navigate to the project folder:
   ```bash
   cd path/to/pdf-file-processing
   ```

3. **Start a local web server**:
   
   **Option A - Using Python (recommended):**
   ```bash
   python3 -m http.server 8000
   ```
   
   **Option B - Using Node.js (if you have it):**
   ```bash
   npx http-server -p 8000
   ```

4. **Open your web browser** and go to:
   ```
   http://localhost:8000/web/
   ```

5. **That's it!** The application should load with the PDF document and CAR references ready to explore.

### How to Use

- **Left Panel**: Browse and filter CAR references
  - Use the search box to find specific references (e.g., "CAR-D29", "CAR-OTP")
  - Click any blue reference tag to filter text blocks
  - Scroll through text blocks containing CAR references

- **Right Panel**: PDF document viewer
  - View the actual PDF content page by page
  - Click any text block on the left to jump to that page
  - Selected text will be highlighted in yellow

- **Resizable Panels**: Drag the divider between panels to resize them

## 📁 Project Structure

```
pdf-file-processing/
├── web/                    # Web application files
│   ├── index.html         # Main web application
│   └── test.html          # Test page for debugging
├── data/                   # Data files (JSON and PDF)
│   ├── pdf_content.json   # Extracted PDF content
│   ├── car_references.json # CAR reference index
│   └── jugement.pdf       # Source PDF document
├── src/                    # Source code for data processing
│   ├── pdf_processor.py    # PDF extraction script
│   ├── extract_car_references.py # CAR reference extraction
│   ├── inspect_json.py     # Data inspection utility
│   └── requirements.txt    # Python dependencies
├── docs/                   # Documentation
├── venv/                   # Python virtual environment
└── README.md              # This file
```

## 🔧 Advanced Usage

### Regenerating Data (Optional)

If you want to process a different PDF or regenerate the data:

1. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r src/requirements.txt
   ```

2. **Extract PDF content**:
   ```bash
   cd src
   python pdf_processor.py ../data/jugement.pdf --use-pdfplumber --output ../data/pdf_content.json
   ```

3. **Extract CAR references**:
   ```bash
   python extract_car_references.py --input ../data/pdf_content.json --output ../data/car_references.json
   ```

### Troubleshooting

**Web app doesn't load?**
- Make sure you're accessing `http://localhost:8000/web/` (note the `/web/` at the end)
- Check that the server is running in the correct directory
- Try a different port: `python3 -m http.server 8080`

**No CAR references showing?**
- Check that `data/car_references.json` exists and contains data
- Open browser developer console (F12) to check for JavaScript errors

**PDF not displaying properly?**
- Ensure `data/pdf_content.json` exists and is not corrupted
- Try refreshing the page

## 📊 Data Information

- **Total Pages**: 1,616 pages
- **CAR References**: 52 unique references found
- **Reference Types**: 
  - CAR-OTP: Prosecutor evidence
  - CAR-D29/D30: Defense evidence  
  - CAR-V45: Victim evidence
- **Text Blocks**: 4,374 blocks containing references

## 🎯 Features

- ✅ Interactive CAR reference browser
- ✅ Real-time search and filtering
- ✅ Click-to-navigate PDF viewer
- ✅ Text highlighting and context display
- ✅ Resizable panels for custom layout
- ✅ Responsive design for different screen sizes
- ✅ No server required - runs entirely in browser

## 🛠️ Technical Details

- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks)
- **PDF Processing**: Python with pdfplumber library
- **Data Format**: JSON for fast client-side processing
- **Browser Compatibility**: Modern browsers with ES6 support
