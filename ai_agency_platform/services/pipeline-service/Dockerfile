FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install heavy ML dependencies first (CPU versions) for better caching
# avoiding the massive CUDA download for torch
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install other heavy/common dependencies that change less frequently
RUN pip install --no-cache-dir chromadb pypdf python-docx sentence-transformers

# Copy requirements from service directory
COPY services/pipeline-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/pipeline-service/app ./app

# Copy shared modules
COPY modules ./modules

# Set Python path to include current directory so 'modules' is discoverable
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8002

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
