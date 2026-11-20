# Veloria technical support assistant: FastAPI backend + static frontend.
#
#   docker compose up --build        (reads ANTHROPIC_API_KEY from .env)
#
# Stage 1 installs dependencies and builds the search indexes (SQLite + Chroma) from data/,
# so the image starts ready to answer. Stage 2 copies only what the app needs at runtime.

ARG PYTHON_VERSION=3.13

# ---------------------------------------------------------------- build
FROM python:${PYTHON_VERSION}-slim AS build

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/opt/hf

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# CPU-only PyTorch: the default Linux wheel bundles CUDA and adds several GB the app never uses.
RUN pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY app/ app/
COPY data/ data/

# Downloads the embedding model into $HF_HOME and builds data/support.db and chroma_db/.
# No API key is needed: ingestion only embeds documents.
RUN python -m app.ingest

# ---------------------------------------------------------------- runtime
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/opt/hf \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1

RUN useradd --create-home --uid 1000 app

COPY --from=build /opt/venv /opt/venv
COPY --from=build /opt/hf /opt/hf

WORKDIR /app
COPY --chown=app:app app/ app/
COPY --chown=app:app frontend/ frontend/
# Chroma and SQLite write lock and journal files next to their data, so the app user owns them.
COPY --from=build --chown=app:app /app/data/ data/
COPY --from=build --chown=app:app /app/chroma_db/ chroma_db/

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
