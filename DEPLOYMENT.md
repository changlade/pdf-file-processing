# PDF Document Explorer - Cloud Run Deployment Guide

This guide covers deploying your PDF Document Explorer to Google Cloud Run with continuous deployment from GitHub.

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud Project** with billing enabled
2. **GitHub repository** containing your code
3. **Databricks token** for semantic search functionality
4. **gcloud CLI** installed and authenticated

### Option 1: Continuous Deployment (Recommended)

Set up automatic deployments from GitHub:

```bash
./setup-cd.sh
```

This script will:
- Enable required GCP APIs
- Connect your GitHub repository to Cloud Build
- Create a Cloud Build trigger for automatic deployments
- Optionally trigger an initial deployment

### Option 2: Manual Deployment

For one-time or manual deployments:

```bash
./deploy.sh
```

## 🔧 Configuration

### Environment Variables

The application requires the following environment variable:

- `DATABRICKS_TOKEN`: Your Databricks API token for semantic search

### Cloud Run Settings

The deployment is configured with:
- **Memory**: 2GB
- **CPU**: 2 vCPU
- **Timeout**: 300 seconds
- **Concurrency**: 80 requests per instance
- **Max instances**: 10
- **Min instances**: 0 (scales to zero)
- **Port**: 8080

## 📁 Project Structure

```
pdf-file-processing/
├── app.py                 # Main Flask application (Cloud Run compatible)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── cloudbuild.yaml       # Cloud Build configuration
├── docker-compose.yml    # Local development
├── setup-cd.sh          # Continuous deployment setup
├── deploy.sh            # Manual deployment script
├── test-local.sh        # Local testing script
├── web/                 # Frontend assets
└── data/               # Application data
```

## 🔄 Continuous Deployment Workflow

1. **Push to main/master branch** → Triggers Cloud Build
2. **Cloud Build** builds Docker image and pushes to Container Registry
3. **Cloud Run** deploys the new image
4. **Health check** verifies deployment success

## 🧪 Local Testing

Test your container locally before deployment:

```bash
# Set your Databricks token
export DATABRICKS_TOKEN="your-token-here"

# Run local tests
./test-local.sh
```

Or use Docker Compose:

```bash
# Set environment variables
export DATABRICKS_TOKEN="your-token-here"

# Start the application
docker-compose up
```

Access the application at: http://localhost:8080

## 🌐 Endpoints

Once deployed, your application will have these endpoints:

- **Main Application**: `https://your-service-url/`
- **Web Interface**: `https://your-service-url/web/`
- **Health Check**: `https://your-service-url/health`
- **Semantic Search**: `https://your-service-url/semantic-search` (POST)
- **RAG Chat**: `https://your-service-url/rag-chat` (POST)

## 🔍 Monitoring

Monitor your deployment through:

- **Cloud Build**: https://console.cloud.google.com/cloud-build/triggers
- **Cloud Run**: https://console.cloud.google.com/run
- **Container Registry**: https://console.cloud.google.com/gcr
- **Logs**: `gcloud logs tail --follow --resource-type=cloud_run_revision`

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Cloud Build logs in the GCP Console
   - Verify `cloudbuild.yaml` syntax
   - Ensure all required files are committed

2. **Deployment Failures**
   - Check Cloud Run logs
   - Verify environment variables are set
   - Ensure service has sufficient resources

3. **Health Check Failures**
   - Verify the `/health` endpoint returns 200
   - Check application startup logs
   - Ensure port 8080 is properly exposed

### Useful Commands

```bash
# View Cloud Run logs
gcloud logs tail --follow --resource-type=cloud_run_revision

# Get service URL
gcloud run services describe pdf-document-explorer --region=us-central1 --format="value(status.url)"

# Update environment variables
gcloud run services update pdf-document-explorer --region=us-central1 --set-env-vars DATABRICKS_TOKEN="new-token"

# Scale service
gcloud run services update pdf-document-explorer --region=us-central1 --max-instances=20
```

## 🔐 Security

- Service runs with a non-root user
- Environment variables are securely managed
- Container follows security best practices
- HTTPS is enforced by Cloud Run

## 💰 Cost Optimization

- **Scales to zero** when not in use
- **Pay-per-request** pricing model
- **Efficient container** with minimal dependencies
- **Resource limits** prevent unexpected costs

## 📞 Support

For issues related to:
- **Cloud Run**: Check GCP documentation
- **Databricks**: Verify token and endpoint configuration
- **Application**: Check application logs and health endpoint
