# Dockerfile for Azure AI Foundry Hosted Agent
# Based on official Microsoft patterns

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent implementation
COPY agent_implementation.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8088

# Expose the port the agent listens on
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8088/health')"

# Run the agent
CMD ["python", "agent_implementation.py"]
