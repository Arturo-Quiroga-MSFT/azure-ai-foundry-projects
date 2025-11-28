# Backend Dockerfile for AG-UI FastAPI Server
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages for code interpreter
RUN pip install --no-cache-dir \
    matplotlib==3.10.7 \
    numpy==2.3.5 \
    pandas==2.3.3 \
    seaborn==0.13.2 \
    tavily-python \
    httpx

# Copy application code
COPY server_magentic.py .
COPY .env.example .env

# Expose port
EXPOSE 8888

# Run the server
CMD ["python", "server_magentic.py"]
