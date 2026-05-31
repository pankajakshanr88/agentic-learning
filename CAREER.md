# From DevOps to Agentic Engineering — the pivot roadmap

The weekend gets you literacy + three agents. This is the rest of the path. The thesis:
**don't compete with ML researchers on modeling — own the operational layer of agents**,
where your DevOps experience is a moat and demand is high.

## The roles you're aiming at

| Title | What it is | How much you already have |
|---|---|---|
| **LLMOps / AI Platform Engineer** | CI/CD, deploy, monitor, eval, cost-control for LLM apps | ~70% — it's DevOps + LLM specifics |
| **Agent Infrastructure Engineer** | Build the runtime/tooling/MCP servers agents run on | ~60% — systems + new protocols |
| **AI/Agent Engineer (product)** | Design & ship agent features | ~40% — needs more prompt/agent design |
| **ML Platform / Reliability** | Serving, GPUs, throughput, SLOs for AI | ~65% — your infra skills transfer |

Pick the first two as targets; they're the least crowded and most you-shaped.

## The gap list (what to learn after the weekend)

Ranked by leverage for someone with your background:

1. **Evals at scale** — datasets, scoring (LLM-as-judge, rubrics), regression suites,
   eval-in-CI gating deploys. *(Your CI/CD instinct is the whole game here.)*
2. **Observability/tracing for agents** — LangSmith / Langfuse / Phoenix; spans per step,
   token & cost dashboards, latency SLOs.
3. **RAG + vector DBs** — embeddings, chunking, retrieval quality, the data pipeline around
   it. The most common "agent" in industry is RAG.
4. **Agent security** — prompt injection, tool sandboxing, least-privilege tool access,
   secrets, output filtering. (OWASP LLM Top 10.) *Maps directly to your IAM/sec work.*
5. **MCP server authoring & hosting** — build and operate tool servers. A clean specialty.
6. **Frameworks fluency** — LangGraph + Claude Agent SDK deep, enough OpenAI SDK to be
   bilingual.
7. **Cost & performance engineering** — caching, model routing, batching, smaller models
   where they suffice.
8. **Deployment patterns** — streaming endpoints, queues for long agent runs, rollback of
   prompts/models like you'd roll back a release.

## Portfolio ladder (build these, in order)

Each should be public, with a README, tests/evals, tracing, and a Dockerfile — i.e., it
should *look operated*, because that's your differentiator.

1. **The capstone** (this weekend) — a small ops agent with an eval + trace + Docker.
2. **A RAG agent over real docs** (e.g., your team's runbooks) with a retrieval eval suite.
3. **An MCP server** exposing a real tool (e.g., a cloud API), plus an agent that uses it.
4. **An "agent platform" mini-project** — deploy an agent with CI-gated evals, a Langfuse/
   LangSmith trace dashboard, cost alerts, and rollback. *This is the portfolio centerpiece;
   it's literally the job.*

## Rough cadence (8–12 weeks, ~6–8 hrs/week post-weekend)

- **Weeks 1–2:** Solidify foundations + prompt/agent design (Anthropic docs, Cookbook).
- **Weeks 3–4:** Evals — build project #2's eval suite; learn LLM-as-judge.
- **Weeks 5–6:** RAG + vector DBs — finish project #2.
- **Weeks 7–8:** MCP — build project #3.
- **Weeks 9–12:** The platform project (#4) + security hardening; write up each project.

## Signal you can show in interviews
- "I treat prompts/models as artifacts: versioned, eval-gated in CI, traced in prod, with
  cost alerts and rollback." — That sentence, *demonstrated*, gets you the LLMOps job.
- Talk in failure modes and SLOs, not just demos. That's the senior signal.
