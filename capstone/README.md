# Capstone: ship one small agent, properly

This is where the weekend lands. Build one agent end to end, and put the operational layer
around it. Keep the agent itself tiny. The ops is the point, and it's the part that proves
you can do this for real.

## The bar

Four things. The agent can be small; all four still have to be there.

1. An agent loop with at least two tools (hand-built from Day 1, or the SDK from lesson 06).
2. Tracing: a structured log per step, including tokens and cost (lesson 07).
3. An eval suite: five cases or more, runnable like a test, exits non-zero on failure
   (lesson 08).
4. Guardrails and a Dockerfile: an allow-list, a max-iterations cap, a cost ceiling, and the
   thing containerized with secrets passed in at runtime (lesson 09 plus `day2_ops/run.md`).

A short README that explains the design, the failure modes, and the rough cost is what makes
it read as the work of someone who's done this before.

## Pick one idea

All four lean on what you already know:

- **Incident triage.** Input: a fake alert plus recent log lines. Tools: `search_logs`,
  `lookup_runbook`, `severity_score`. Output: likely cause and a first action.
- **CI-failure explainer.** Input: a build log. Tools: `extract_errors`,
  `search_known_issues`. Output: the cause in plain English and which file or test to open.
- **Cloud-cost analyst.** Input: a fake billing CSV. Tools: `query_costs`, `calculator`.
  Output: the top cost drivers and one optimization, with the math shown.
- **Runbook RAG.** Index a folder of markdown runbooks and answer questions with citations.
  This one introduces retrieval, which is your on-ramp to RAG in CAREER.md.

## A 3 to 4 hour plan

1. 30 min: pick the idea and write the eval cases first. Decide what "good" looks like.
2. 90 min: build the loop and the tools until the evals pass.
3. 45 min: add tracing and guardrails.
4. 30 min: write the Dockerfile and a README with design notes and failure modes.
5. 15 min: run the eval suite once more and commit.

## Done means

- `python eval.py` passes and exits 0; breaking the prompt makes it exit 1.
- `docker build` works, and `docker run` shows a traced run.
- The README covers what it does, the tools, the guardrails, the failure modes, and the cost.

Push it to GitHub and you have something concrete to point at, and it shows the exact mix
LLMOps roles hire for. Next is [CAREER.md](../CAREER.md).
