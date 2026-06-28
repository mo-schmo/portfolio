FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/cache/hf \
    SENTENCE_TRANSFORMERS_HOME=/cache/hf

WORKDIR /app

# System deps for sentence-transformers / numpy.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Pre-download the embedding model so the first request is fast and the
# container works in air-gapped environments.
RUN python -c "import os; from sentence_transformers import SentenceTransformer; \
    SentenceTransformer(os.environ.get('EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5'))"

COPY app ./app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
