FROM python:3.11-slim

LABEL maintainer="Backend Architect"
LABEL description="EXHUMED - FastAPI Backend"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt ./backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY backend ./backend
COPY static ./static

# Run the application
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}