# PDF Document Explorer

A powerful PDF viewer with AI-powered semantic search capabilities, designed for deployment on Google Cloud Run.

## 🚀 Features

- **📄 PDF Viewing**: Full-featured PDF viewer with page navigation
- **🔍 CAR Reference Search**: Search for specific document references
- **🧠 Semantic Search**: AI-powered search using Databricks Vector Search
- **💬 RAG Chat**: Interactive AI chatbot for document questions
- **🎯 Smart Navigation**: Click on search results to jump to specific PDF pages
- **📱 Responsive UI**: Modern, clean interface optimized for web deployment
- **☁️ Cloud Ready**: Containerized for Google Cloud Run deployment

## 📁 Project Structure

```
pdf-file-processing/
├── 📄 README.md                # This documentation
├── 🐍 app.py                   # Main Flask application
├── 🐳 Dockerfile               # Container configuration
├── 📋 requirements.txt         # Python dependencies
├── 🔧 .dockerignore            # Docker build optimization
├── 🔒 env.example              # Environment variables template
├── 📂 web/                     # Frontend files
│   └── index.html              # Main application UI
└── 📂 data/                    # Application data
    ├── car_references.json     # CAR reference database
    ├── pdf_content.json        # PDF content blocks
    └── jugement.pdf            # Sample PDF document
```

## 🚀 Quick Deployment to Cloud Run

### Prerequisites
- Google Cloud Project with billing enabled
- GitHub repository containing this code
- Databricks token for semantic search functionality

### Deploy Steps

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy PDF Document Explorer"
   git push origin main
   ```

2. **Set up Cloud Run service**:
   - Go to [Google Cloud Run Console](https://console.cloud.google.com/run)
   - Click **"Create Service"**
   - Select **"Continuously deploy from a repository"**
   - Connect your GitHub repository
   - Configure:
     - **Service name**: `pdf-document-explorer`
     - **Region**: `us-central1` (or your preferred region)
     - **Authentication**: Allow unauthenticated invocations
     - **Memory**: 2 GiB
     - **CPU**: 2
     - **Environment variable**: `DATABRICKS_TOKEN` = `your-actual-token`

3. **Automatic deployments**: Every push to `main` will now automatically deploy!

## 🔧 Local Development

### Using Docker (Recommended)

```bash
# Set your Databricks token
export DATABRICKS_TOKEN="your-actual-databricks-token"

# Build and run the container
docker build -t pdf-explorer .
docker run -p 8080:8080 -e DATABRICKS_TOKEN="$DATABRICKS_TOKEN" pdf-explorer

# Access the application
open http://localhost:8080
```

### Direct Python Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABRICKS_TOKEN="your-actual-databricks-token"
export PORT=8080

# Run the application
python app.py

# Access the application
open http://localhost:8080
```

## 🔐 Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```bash
# Copy the template
cp env.example .env

# Edit with your values
DATABRICKS_TOKEN=your-actual-databricks-token
```

### Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABRICKS_TOKEN` | Yes | Your Databricks API token for semantic search |
| `DATABRICKS_URL` | No | Override default Databricks endpoint |
| `RAG_URL` | No | Override default RAG endpoint |
| `PORT` | No | Port number (default: 8080) |

## 🌐 Application Endpoints

Once deployed, your application provides:

- **Main Application**: `/` - PDF viewer interface
- **Web Interface**: `/web/` - Alternative entry point
- **Health Check**: `/health` - Service health status
- **Semantic Search**: `/semantic-search` (POST) - AI-powered search API
- **RAG Chat**: `/rag-chat` (POST) - Interactive AI chatbot API
- **Data Files**: `/data/<filename>` - Access to PDF and JSON data

## 🎯 Usage

### PDF Viewing
1. The application loads with the sample PDF document
2. Use the navigation controls to browse pages
3. Zoom in/out and navigate as needed

### Search Modes

#### CAR Reference Search
- Search for specific document references (e.g., "CAR/123")
- Results show reference counts and locations in the document
- Click results to jump to relevant pages

#### Semantic Search
- AI-powered contextual search (e.g., "war crimes evidence")
- Results show similarity scores and content summaries
- Powered by Databricks Vector Search
- Click results to navigate to relevant document sections

#### RAG Chat
- Interactive AI chatbot for document questions
- Ask natural language questions about the document content
- Get contextual answers based on the document

## 🏗️ Architecture

- **Frontend**: HTML/CSS/JavaScript with PDF.js for PDF rendering
- **Backend**: Python Flask application with CORS support
- **Container**: Docker with optimized Python 3.11 slim image
- **Search**: Databricks Vector Search API integration
- **Chat**: Databricks RAG (Retrieval-Augmented Generation) API
- **Deployment**: Google Cloud Run with automatic scaling

## 🔍 API Usage

### Semantic Search API

```bash
curl -X POST http://localhost:8080/semantic-search \
  -H "Content-Type: application/json" \
  -d '{"query": "war crimes evidence", "get_all": false}'
```

### RAG Chat API

```bash
curl -X POST http://localhost:8080/rag-chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What evidence is mentioned in the document?", "num_results": [10], "conversation_id": ["session_001"]}'
```

## 🛠️ Development Notes

### Container Optimization
- Uses Python 3.11 slim base image for security and performance
- Multi-stage build process for minimal image size
- Non-root user for enhanced security
- Health checks for Cloud Run compatibility
- Optimized gunicorn configuration for production

### Security Features
- Environment variables for sensitive configuration
- No secrets stored in code or repository
- HTTPS enforced by Cloud Run
- Container runs as non-root user
- Minimal attack surface with slim base image

### Performance
- Scales to zero when not in use (cost-effective)
- Fast cold start times with optimized container
- Efficient caching with Docker layer optimization
- Gunicorn with optimal worker/thread configuration

## 🚨 Troubleshooting

### Common Issues

1. **Semantic Search Not Working**
   - Verify `DATABRICKS_TOKEN` environment variable is set
   - Check internet connectivity for API access
   - Verify Databricks endpoints are accessible

2. **Container Build Failures**
   - Ensure Docker is running
   - Check Dockerfile syntax
   - Verify all required files are present

3. **Cloud Run Deployment Issues**
   - Check Cloud Run logs in Google Cloud Console
   - Verify environment variables are set in Cloud Run
   - Ensure service has sufficient memory/CPU allocation

### Useful Commands

```bash
# Check container logs
docker logs <container-id>

# Test health endpoint
curl http://localhost:8080/health

# View Cloud Run logs (if deployed)
gcloud logs tail --follow --resource-type=cloud_run_revision

# Update Cloud Run environment variables
gcloud run services update pdf-document-explorer \
  --region=us-central1 \
  --set-env-vars DATABRICKS_TOKEN="new-token"
```

## 📝 License

This project is for internal use and demonstration purposes.

---

**Version**: 3.0.0 - Cloud Run Ready  
**Last Updated**: September 2025