FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any are needed (none required for standard python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first to cache dependency installation
COPY pyproject.toml .

# Install dependencies using pip
RUN pip install --no-cache-dir .

# Copy source code
COPY server.py .
COPY scraper.py .
COPY README.md .

# Expose port for SSE transport (if used)
EXPOSE 8000

# Default entrypoint runs server.py in stdio mode. 
# To run in SSE mode, override command with "--transport sse --port 8000"
ENTRYPOINT ["python", "server.py"]
CMD ["--transport", "stdio"]
