# Containerizing the agent

An agent ships like any other service, and this Dockerfile is deliberately boring — that's the
point. The only agent-specific habits are how you handle the API key and that you run as a
non-root user. Everything else is the same packaging you do every week.

## Reading the Dockerfile

Dependencies first, for layer caching — your usual Docker instinct applies unchanged.

```dockerfile
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
```

Then the two things worth calling out. Run as a non-root user — least privilege for the container,
just like everywhere else. And note what we *don't* do: the API key is never baked into the
image.

```dockerfile
RUN useradd --create-home appuser
USER appuser

CMD ["python", "day2_ops/07_tracing.py"]
```

The key comes in at runtime instead:

```bash
docker build -t weekend-agent -f day2_ops/Dockerfile .
docker run --rm -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" weekend-agent
```

In production that `-e` becomes a secrets manager — Vault, a cloud secret store, a Kubernetes
Secret — which is exactly what you already do for every other service's credentials.

## What to watch for

- Never bake the key into the image. Images get pushed to registries and shared; secrets passed at
  runtime don't travel with them.
- The default `CMD` runs the traced agent so a plain `docker run` shows you structured output. In a
  real service you'd point it at your entrypoint.
- An agent run can take minutes. For real workloads you wouldn't hold an HTTP connection open for
  one — see the deploy-shapes notes in "Running in Production."

## Recap

- An agent containerizes like any service; most of this is your normal Dockerfile.
- Pass the API key at runtime via env or a secrets manager, never in the image.
- Run as non-root for least privilege.
- The interesting operational questions (long runs, queues, scaling) live in the run notes, not the
  Dockerfile.
