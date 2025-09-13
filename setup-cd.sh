#!/bin/bash

# PDF Document Explorer - Cloud Build Continuous Deployment Setup
# This script sets up continuous deployment from GitHub to Cloud Run using Cloud Build

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
GITHUB_REPO=""  # Format: owner/repo-name
DATABRICKS_TOKEN=""

echo -e "${BLUE}🔄 PDF Document Explorer - Continuous Deployment Setup${NC}"
echo "========================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
    echo "Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
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

# Get GitHub repository if not set
if [ -z "$GITHUB_REPO" ]; then
    echo -e "${YELLOW}📝 Please enter your GitHub repository (format: owner/repo-name):${NC}"
    read GITHUB_REPO
    
    if [ -z "$GITHUB_REPO" ]; then
        echo -e "${RED}❌ Error: GitHub repository is required${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Using GitHub Repository: ${GITHUB_REPO}${NC}"

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
gcloud services enable sourcerepo.googleapis.com

# Connect GitHub repository to Cloud Build
echo -e "${BLUE}🔗 Connecting GitHub repository to Cloud Build...${NC}"
echo -e "${YELLOW}📋 You'll need to authorize Cloud Build to access your GitHub repository.${NC}"
echo -e "${YELLOW}    This will open a browser window for authentication.${NC}"
echo -e "${YELLOW}    Press Enter to continue...${NC}"
read

# Create the Cloud Build trigger
echo -e "${BLUE}🚀 Creating Cloud Build trigger...${NC}"
gcloud builds triggers create github \
    --repo-name="$(echo $GITHUB_REPO | cut -d'/' -f2)" \
    --repo-owner="$(echo $GITHUB_REPO | cut -d'/' -f1)" \
    --branch-pattern="^main$|^master$" \
    --build-config="cloudbuild.yaml" \
    --substitutions="_DATABRICKS_TOKEN=$DATABRICKS_TOKEN" \
    --name="pdf-document-explorer-cd" \
    --description="Continuous deployment for PDF Document Explorer"

echo -e "${GREEN}✅ Cloud Build trigger created successfully!${NC}"

# Initial deployment (optional)
echo -e "${YELLOW}🤔 Would you like to trigger an initial deployment now? (y/n):${NC}"
read -r DEPLOY_NOW

if [[ $DEPLOY_NOW =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🚀 Triggering initial deployment...${NC}"
    
    # Run the build manually for the first time
    gcloud builds submit \
        --config cloudbuild.yaml \
        --substitutions _DATABRICKS_TOKEN="$DATABRICKS_TOKEN" \
        .
    
    # Get the service URL
    echo -e "${BLUE}🌐 Getting service URL...${NC}"
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")
    
    if [ -n "$SERVICE_URL" ]; then
        echo -e "${GREEN}🎉 Initial deployment successful!${NC}"
        echo -e "${GREEN}📱 Your PDF Document Explorer is live at: ${BLUE}$SERVICE_URL${NC}"
    else
        echo -e "${YELLOW}⚠️  Service URL not available yet. Check Cloud Run console.${NC}"
    fi
fi

echo
echo -e "${GREEN}🎉 Continuous Deployment Setup Complete!${NC}"
echo "========================================================"
echo -e "${GREEN}✅ What's been set up:${NC}"
echo -e "   • Cloud Build trigger connected to ${BLUE}$GITHUB_REPO${NC}"
echo -e "   • Automatic deployments on push to main/master branch"
echo -e "   • Container registry configured"
echo -e "   • Cloud Run service configured"
echo
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "   1. Push your code to the ${BLUE}main${NC} or ${BLUE}master${NC} branch"
echo -e "   2. Cloud Build will automatically:"
echo -e "      • Build your Docker container"
echo -e "      • Push to Container Registry"
echo -e "      • Deploy to Cloud Run"
echo -e "      • Run health checks"
echo
echo -e "${BLUE}🔍 Monitor your deployments:${NC}"
echo -e "   • Cloud Build: https://console.cloud.google.com/cloud-build/triggers"
echo -e "   • Cloud Run: https://console.cloud.google.com/run"
echo -e "   • Container Registry: https://console.cloud.google.com/gcr"
echo
echo -e "${GREEN}🚀 Happy deploying!${NC}"
