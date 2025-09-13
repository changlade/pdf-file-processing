#!/bin/bash

# Local testing script for PDF Document Explorer
# Tests the Docker container locally before deploying to Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Testing PDF Document Explorer locally${NC}"
echo "=========================================="

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Build the Docker image
echo -e "${BLUE}🏗️  Building Docker image...${NC}"
docker build -t pdf-document-explorer:test .

# Stop any existing container
echo -e "${BLUE}🛑 Stopping any existing containers...${NC}"
docker stop pdf-explorer-test 2>/dev/null || true
docker rm pdf-explorer-test 2>/dev/null || true

# Run the container
echo -e "${BLUE}🚀 Starting container...${NC}"
docker run -d \
    --name pdf-explorer-test \
    -p 8080:8080 \
    -e DATABRICKS_TOKEN="${DATABRICKS_TOKEN:-test-token}" \
    pdf-document-explorer:test

# Wait for container to start
echo -e "${BLUE}⏳ Waiting for container to start...${NC}"
sleep 5

# Test health endpoint
echo -e "${BLUE}🔍 Testing health endpoint...${NC}"
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo -e "${YELLOW}📋 Container logs:${NC}"
    docker logs pdf-explorer-test
    docker stop pdf-explorer-test
    docker rm pdf-explorer-test
    exit 1
fi

# Test main application
echo -e "${BLUE}🔍 Testing main application...${NC}"
if curl -f http://localhost:8080/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Main application accessible${NC}"
else
    echo -e "${RED}❌ Main application not accessible${NC}"
    echo -e "${YELLOW}📋 Container logs:${NC}"
    docker logs pdf-explorer-test
    docker stop pdf-explorer-test
    docker rm pdf-explorer-test
    exit 1
fi

echo -e "${GREEN}🎉 Local testing successful!${NC}"
echo "=========================================="
echo -e "${GREEN}📱 Your application is running at:${NC}"
echo -e "${BLUE}http://localhost:8080${NC}"
echo
echo -e "${YELLOW}📋 Available endpoints:${NC}"
echo -e "   • Main app: ${BLUE}http://localhost:8080${NC}"
echo -e "   • Web interface: ${BLUE}http://localhost:8080/web/${NC}"
echo -e "   • Health check: ${BLUE}http://localhost:8080/health${NC}"
echo -e "   • Semantic search: ${BLUE}http://localhost:8080/semantic-search${NC} (POST)"
echo -e "   • RAG chat: ${BLUE}http://localhost:8080/rag-chat${NC} (POST)"
echo
echo -e "${YELLOW}🛑 To stop the container:${NC}"
echo "   docker stop pdf-explorer-test && docker rm pdf-explorer-test"
echo
echo -e "${GREEN}✅ Ready for Cloud Run deployment!${NC}"
