# Running an agent like a real service

![Dashboards and performance graphs on a screen](../vendor/img/observability.jpg)

An agent is a service with two twists: the core is stochastic, and one dependency (the model
API) is metered. Almost nothing else about operating it is new to you. Here's the mapping.

## Build and run the container

```bash
# from the repo root ("Agentic learning")
docker build -t weekend-agent -f day2_ops/Dockerfile .
docker run --rm -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" weekend-agent
```

The key is passed in at runtime, never baked into the image. In prod that's a secrets
manager (Vault, the cloud's secret store, a Kubernetes Secret), which is what you already do.

## The ops checklist, next to what you already know

| Concern | For a normal service | For an agent, also |
|---------|----------------------|--------------------|
| Secrets | env or a secrets manager | the same, plus rotate the model API key |
| Rate limits | client throttling, backoff | the model API has RPM and TPM limits; handle 429s |
| Cost | cloud budget alerts | per-request token cost; alert on dollars per run (lesson 07) |
| Latency | p99 SLOs | model calls are slow and variable; stream, set timeouts |
| Long runs | a sync request | a run can take minutes; use a queue and a worker, not a blocking handler |
| Observability | logs, metrics, traces | per-step traces with tokens and tool I/O (lesson 07) |
| Releases | versioned deploys, rollback | version the prompt and model too, and eval-gate them (lesson 08) |
| Safety | input validation, WAF, IAM | plus prompt injection and tool allow-lists (lesson 09) |
| Quality gate | tests in CI | evals in CI (lesson 08) |

## Deploy shapes

- Short tasks: a containerized HTTP service with streaming responses and timeouts.
- Long or agentic tasks: enqueue the job, let a worker run the loop, and have the client poll
  or get a webhook. Don't hold an HTTP connection open for a three-minute run.
- Scale: model calls are I/O-bound, so concurrency is your lever, not CPU. Watch the TPM
  limit.

## What makes a project look operated

For your portfolio (see [CAREER.md](../CAREER.md)), every agent you publish should ship with
a Dockerfile, runtime secrets, a trace, an eval suite in CI, and a note on cost and latency.
That set is what convinces a hiring manager you can run agents in production, because you can.
