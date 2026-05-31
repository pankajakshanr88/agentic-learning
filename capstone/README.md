# Capstone — ship one small, *operated* agent

Goal: prove the whole weekend stuck by building ONE agent end to end — with the ops layer
that makes it your differentiator. Scope it small; finish it completely.

## The bar (this is the portfolio piece)

Your agent must have all four. The agent itself can be tiny — the ops layer is the point.

1. **An agent loop** with at least 2 tools (DIY from Day 1, or the SDK from Lesson 06).
2. **Tracing** — structured per-step logs incl. tokens + cost (Lesson 07).
3. **An eval suite** — ≥5 cases, runnable like a test, non-zero exit on failure (Lesson 08).
4. **Guardrails + a Dockerfile** — allow-list, max-iterations, cost ceiling; containerized
   with runtime secrets (Lesson 09 + run.md).

A short README explaining the design, failure modes, and cost/latency = the senior signal.

## Pick one idea (all DevOps-flavored on purpose)

- **Incident-triage agent** — input: a (fake) alert + recent log lines. Tools: `search_logs`,
  `lookup_runbook`, `severity_score`. Output: likely cause + suggested first action.
- **CI-failure explainer** — input: a build log. Tools: `extract_errors`, `search_known_issues`.
  Output: plain-English cause + which file/test to look at.
- **Cloud-cost analyst** — input: a (fake) billing CSV. Tools: `query_costs`, `calculator`.
  Output: top cost drivers + one optimization, with the math shown.
- **Runbook RAG agent** — index a folder of markdown runbooks; answer ops questions with
  citations. (Stretch: introduces retrieval — your on-ramp to RAG in CAREER.md.)

## Suggested 3–4 hour plan

1. **30 min** — pick the idea; write the eval cases FIRST (what does "good" look like?).
2. **90 min** — build the agent loop + tools until the evals pass.
3. **45 min** — add tracing + guardrails.
4. **30 min** — Dockerfile + a README with design notes and failure modes.
5. **15 min** — run the eval suite one last time; commit. Done.

## Definition of done
- `python eval.py` passes and exits 0; breaking the prompt makes it exit 1.
- `docker build` succeeds; `docker run` shows a traced run.
- README explains: what it does, the tools, the guardrails, known failure modes, rough cost.

When this is on your GitHub, you have something concrete to point at in an interview — and
it demonstrates the exact thing LLMOps roles are hiring for. Next steps: CAREER.md.
