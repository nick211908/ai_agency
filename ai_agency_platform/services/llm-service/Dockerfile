FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY services/llm-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/llm-service/app ./app

# Expose port
EXPOSE 8003

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
