# ---------- Stage 1: Builder ----------
FROM python:3.14-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: Production ----------
FROM python:3.14-slim

# Create non-root user
RUN useradd \
    --create-home \
    --shell /bin/bash \
    appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application
COPY app/ /app/

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Application port
EXPOSE 5000

# Health check
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run as non-root user
USER appuser

# Start application
CMD ["python", "app.py"]
