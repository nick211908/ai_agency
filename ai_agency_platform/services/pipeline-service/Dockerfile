# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# If you later add sentence-transformers, install CPU-only torch first to avoid massive CUDA wheels:
# RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
#  && pip install --no-cache-dir sentence-transformers

COPY app ./app

USER app
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
