# Use Python 3.11 slim image for better performance and security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Install system dependencies and clean up in single layer
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# Copy application code
COPY app.py .
COPY web/ ./web/
COPY data/ ./data/

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 app \
    && chown -R app:app /app
USER app

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Expose the port that Cloud Run expects
EXPOSE 8080

# Use gunicorn with optimized settings for Cloud Run
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    app:app
