FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements from service directory
COPY services/auth-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/auth-service/app ./app

# Expose port
EXPOSE 8001

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
