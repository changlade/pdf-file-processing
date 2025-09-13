#!/bin/bash

# PDF Document Explorer - GCP Cloud Run Deployment Script
# This script builds and deploys the application to Google Cloud Run

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=""
REGION="us-central1"
SERVICE_NAME="pdf-document-explorer"
DATABRICKS_TOKEN=""

echo -e "${BLUE}🚀 PDF Document Explorer - Cloud Run Deployment${NC}"
echo "=================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
    echo "Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Get project ID if not set
if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}📝 Getting current GCP project...${NC}"
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ Error: No GCP project set${NC}"
        echo "Please set your project: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Using GCP Project: ${PROJECT_ID}${NC}"

# Get Databricks token if not set
if [ -z "$DATABRICKS_TOKEN" ]; then
    echo -e "${YELLOW}🔑 Please enter your Databricks token:${NC}"
    read -s DATABRICKS_TOKEN
    echo
    
    if [ -z "$DATABRICKS_TOKEN" ]; then
        echo -e "${RED}❌ Error: Databricks token is required${NC}"
        exit 1
    fi
fi

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required GCP APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo -e "${BLUE}🏗️  Building and deploying with Cloud Build...${NC}"
gcloud builds submit \
    --config cloudbuild.yaml \
    --substitutions _DATABRICKS_TOKEN="$DATABRICKS_TOKEN" \
    .

# Get the service URL
echo -e "${BLUE}🌐 Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

if [ -n "$SERVICE_URL" ]; then
    echo -e "${GREEN}🎉 Deployment successful!${NC}"
    echo "=================================================="
    echo -e "${GREEN}📱 Your PDF Document Explorer is now live at:${NC}"
    echo -e "${BLUE}$SERVICE_URL${NC}"
    echo
    echo -e "${GREEN}🔗 Direct links:${NC}"
    echo -e "   • Main app: ${BLUE}$SERVICE_URL${NC}"
    echo -e "   • Health check: ${BLUE}$SERVICE_URL/health${NC}"
    echo
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "   1. Test your application at the URL above"
    echo "   2. Configure custom domain (optional)"
    echo "   3. Set up monitoring and logging"
    echo
    echo -e "${GREEN}✅ Deployment complete!${NC}"
else
    echo -e "${RED}❌ Error: Could not retrieve service URL${NC}"
    echo "Please check the Cloud Run console for more details."
    exit 1
fi
