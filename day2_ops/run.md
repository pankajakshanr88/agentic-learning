# Running an agent like a real service

You operate services for a living — an agent is just a service with a stochastic core and
a metered dependency (the model API). The ops checklist barely changes; here's the mapping.

## Build & run the container

```bash
# from the repo root ("Agentic learning")
docker build -t weekend-agent -f day2_ops/Dockerfile .
docker run --rm -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" weekend-agent
```

The key is passed at **runtime**, never baked into the image. In prod that's a secrets
manager (Vault, AWS/GCP secret manager, k8s Secret) — exactly what you already do.

## The ops checklist for agents (vs. what you already know)

| Concern | For a normal service you… | For an agent, additionally… |
|---|---|---|
| **Secrets** | env / secrets manager | same — plus rotate the model API key |
| **Rate limits** | client-side throttling, retries w/ backoff | the model API has RPM/TPM limits — handle 429s |
| **Cost** | cloud budget alerts | **per-request token cost** — alert on $/run (Lesson 07) |
| **Latency** | p99 SLOs | model calls are slow + variable; stream, set timeouts |
| **Long runs** | sync request | agent runs can take minutes — use a **queue/worker**, not a blocking HTTP handler |
| **Observability** | logs/metrics/traces | per-step traces incl. tokens/tool I/O (Lesson 07) |
| **Releases** | versioned deploys, rollback | version the **prompt + model** too; eval-gate them (Lesson 08) |
| **Safety** | input validation, WAF, IAM | + prompt injection, tool allow-lists (Lesson 09) |
| **Quality gate** | unit/integration tests in CI | **evals in CI** (Lesson 08) |

## Deploy shapes
- **Short tasks:** containerized HTTP service with streaming responses + timeouts.
- **Long/agentic tasks:** enqueue the job; a worker runs the agent loop; client polls or
  gets a webhook. Don't hold an HTTP connection open for a 3-minute agent run.
- **Scale:** model API calls are I/O-bound — concurrency, not CPU, is your lever. Mind TPM.

## The "operated" signal
For your portfolio (see CAREER.md), every agent you publish should ship with: a Dockerfile,
runtime secrets, a trace, an eval suite in CI, and notes on cost/latency. That trifecta is
what makes a hiring manager believe you can run agents in production — because you can.
