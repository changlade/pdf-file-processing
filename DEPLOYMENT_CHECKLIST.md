# Cloud Run Deployment Checklist

## ✅ Data Files Ready for Deployment

All data files have been regenerated from **JUDGMENT.pdf** (October 23, 2025):

### Required Data Files (all in `data/` folder):
- ✅ **JUDGMENT.pdf** (18 MB) - Source PDF document with 1,649 pages
- ✅ **car_references.json** (2 MB) - Contains all CAR references with optimized reference_index
  - 3,689 unique references
  - 1,306 blocks with references
  - Includes reference_index for fast lookups
- ✅ **block_content.json** (4 MB) - Full text content for each block
  - 1,306 blocks
- ✅ **pdf_content.json** (5 MB) - Complete PDF text extraction
  - 1,649 pages
  - 711,595 words

### Files Excluded from Deployment (via .dockerignore):
- ❌ JUDGMENT_parsed.csv - Not used by the app
- ❌ Extract scripts (extract_*.py, optimize_references.py)
- ❌ Old optimized files (*_optimized.json)

## 📊 Statistics Comparison

| Metric | Old (jugement.pdf) | New (JUDGMENT.pdf) |
|--------|-------------------|-------------------|
| Pages | 1,616 | 1,649 (+33) |
| References | 2,297 | 3,689 (+1,392) |
| Reference Blocks | 1,274 | 1,306 (+32) |
| Evidence Codes | 2,027 | 3,442 (+1,415) |
| Witness Codes | 270 | 247 (-23) |

## 🚀 Deployment Steps

### 1. Verify Local Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Test the app locally
python app.py
# Visit http://localhost:8080

# Verify data loads correctly
curl http://localhost:8080/data/car_references.json | jq '.extraction_info'
```

### 2. Build Docker Image
```bash
# Build the image
docker build -t pdf-explorer .

# Test the Docker image locally
docker run -p 8080:8080 -e PORT=8080 pdf-explorer

# Visit http://localhost:8080 and verify:
# - CAR references load
# - PDF displays
# - Text blocks appear when clicking references
```

### 3. Deploy to Cloud Run
```bash
# Configure gcloud (if not already done)
gcloud config set project YOUR_PROJECT_ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pdf-explorer

# Deploy to Cloud Run
gcloud run deploy pdf-explorer \
  --image gcr.io/YOUR_PROJECT_ID/pdf-explorer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300s \
  --max-instances 10
```

### 4. Verify Deployment
After deployment, test these URLs:
- `https://YOUR-SERVICE-URL/` - Main app
- `https://YOUR-SERVICE-URL/health` - Health check
- `https://YOUR-SERVICE-URL/data/car_references.json` - Data file
- `https://YOUR-SERVICE-URL/data/JUDGMENT.pdf` - PDF file

## ⚠️ Common Issues & Solutions

### Issue: "Failed to load data files"
**Solution**: 
- Check that all JSON files are in the `data/` folder
- Verify JSON files are valid: `python3 -m json.tool data/car_references.json > /dev/null`
- Check browser console for specific error messages

### Issue: "References not displaying"
**Solution**:
- Verify `car_references.json` contains `reference_index` field
- Check structure: `jq '.reference_index | keys | length' data/car_references.json`
- Should return: 3689

### Issue: "PDF not loading"
**Solution**:
- Verify JUDGMENT.pdf exists in data folder
- Check file size: `ls -lh data/JUDGMENT.pdf` (should be ~18MB)
- Test PDF access: `curl -I http://localhost:8080/data/JUDGMENT.pdf`

### Issue: Docker image too large
**Solution**:
- Verify .dockerignore is properly configured
- Check image size: `docker images pdf-explorer`
- Should be < 500MB

### Issue: Cloud Run timeout
**Solution**:
- Increase timeout in deployment: `--timeout 300s`
- Increase memory: `--memory 2Gi`
- Check logs: `gcloud run logs read pdf-explorer`

## 📝 Environment Variables

No environment variables are required for basic operation. The app is fully self-contained.

## 🔒 Security Notes

- The app runs as non-root user (uid 1000) in Docker
- All files are served as static content
- No sensitive data or credentials required
- CORS is enabled for web access

## 📦 Total Deployment Size

- Data folder: ~29 MB (after excluding CSV and optimized files)
- Docker image: ~200-300 MB (estimated)
- Cloud Run memory: 2 GB recommended

## ✅ Final Verification Checklist

Before deploying, verify:
- [ ] All JSON files have been regenerated from JUDGMENT.pdf
- [ ] `car_references.json` contains `reference_index`
- [ ] Old `jugement.pdf` has been removed
- [ ] App works locally with new data
- [ ] Docker image builds successfully
- [ ] .dockerignore excludes unnecessary files
- [ ] Dockerfile copies all required files from data/ folder

