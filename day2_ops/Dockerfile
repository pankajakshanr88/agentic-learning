# Day 2 (OPS) — Containerize an agent like any other service.
# Build:  docker build -t weekend-agent -f day2_ops/Dockerfile .
# Run:    docker run --rm -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY weekend-agent
#
# Notice what we DON'T do: bake the API key into the image. Secrets come in at runtime
# via -e / a secrets manager — same hygiene as any service you operate. See run.md.

FROM python:3.12-slim

WORKDIR /app

# Install deps first for layer caching (your usual Docker instinct applies).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the lessons (in real life: just your agent's source).
COPY . .

# Run as non-root — least privilege for the container, too.
RUN useradd --create-home appuser
USER appuser

# Default: run the traced agent so a `docker run` shows structured output.
CMD ["python", "day2_ops/07_tracing.py"]
