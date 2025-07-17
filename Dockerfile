# FROM python:3.9-slim

# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . .

# # Expose the Flask port
# EXPOSE 5000

# # Run the application
# CMD ["python", "app.py"]

FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Runtime configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

# Health check endpoint (add this to your app.py)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]