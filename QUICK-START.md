# 🚀 Quick Start - PDF Document Explorer on Cloud Run

## ✅ Ready to Deploy!

Your PDF Document Explorer is now containerized and ready for continuous deployment to Google Cloud Run.

## 🎯 **Next Steps (5 minutes setup):**

### 1. **Set up Continuous Deployment**
```bash
./setup-cd.sh
```

This interactive script will:
- ✅ Enable required GCP APIs
- 🔗 Connect your GitHub repository to Cloud Build
- 🚀 Create automatic deployment triggers
- 🎯 Optionally trigger initial deployment

### 2. **Test Locally (Optional)**
```bash
# Set your Databricks token
export DATABRICKS_TOKEN="your-actual-token"

# Test the container
./test-local.sh
```

### 3. **Push to GitHub**
Once setup is complete, every push to `main` or `master` will automatically:
1. Build your container
2. Deploy to Cloud Run
3. Run health checks

## 📁 **What's Been Created:**

### **Core Application Files:**
- `app.py` - Cloud Run compatible Flask app
- `Dockerfile` - Optimized container
- `requirements.txt` - Python dependencies

### **Deployment Configuration:**
- `cloudbuild.yaml` - Cloud Build pipeline
- `setup-cd.sh` - Continuous deployment setup
- `deploy.sh` - Manual deployment option

### **Testing & Development:**
- `test-local.sh` - Local container testing
- `docker-compose.yml` - Local development
- `.dockerignore` - Optimized builds

### **Documentation:**
- `DEPLOYMENT.md` - Complete deployment guide
- `QUICK-START.md` - This file

## 🌐 **Your App Endpoints (after deployment):**

- **Main App**: `https://your-service-url/`
- **Web Interface**: `https://your-service-url/web/`
- **Health Check**: `https://your-service-url/health`
- **Semantic Search API**: `https://your-service-url/semantic-search`
- **RAG Chat API**: `https://your-service-url/rag-chat`

## 🔑 **Required:**

1. **Google Cloud Project** with billing enabled
2. **GitHub repository** (this code needs to be pushed)
3. **Databricks token** for semantic search functionality

## 🚀 **Ready? Run this command:**

```bash
./setup-cd.sh
```

The script will guide you through the entire setup process!
