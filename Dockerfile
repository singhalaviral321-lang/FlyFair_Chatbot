FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps kept minimal (faiss-cpu works without extra libs)
WORKDIR /app/backend

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

EXPOSE 8000

# Railway provides $PORT at runtime
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

