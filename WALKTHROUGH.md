# WALKTHROUGH.md — facilitator guide (for you, the teacher)

This is the *teacher view*. She follows README.md; you use this to lead. Format per module:
**point** (what to land), **show** (what to run), **ask** (a question to check understanding),
**watch for** (common confusion).

> Pacing: Day 1 is ~5–6h, Day 2 ~6–7h. Take breaks after each numbered file. Let her *type*
> the "Your turn" blocks herself — don't drive the keyboard the whole time.

---

## Before you start (10 min)
- Do SETUP.md together; confirm `python day1/01_hello_llm.py` prints a reply.
- Land the one-sentence frame: *"An LLM is a stateless function; an agent is a loop that lets
  it use tools."* Everything hangs off that.

## Day 1

### 01_hello_llm.py — the function
- **Point:** text in → text out, stateless. Roles (system/user/assistant). Tokens = cost.
- **Show:** run it; then run it twice and note it has no memory of the first call.
- **Ask:** "If it's stateless, how would a chatbot remember your name?" (Answer: you resend
  the history every call — that's the trick.)
- **Watch for:** thinking the model "remembers." It doesn't; the *caller* does.

### 02_first_tool.py — giving it hands
- **Point:** the model can't run code; it *asks* you to, via a structured tool call. You run
  it, return the result. This is the entire basis of agents.
- **Show:** run it; print the raw tool-call request before executing it so she sees the JSON.
- **Ask:** "Who actually executes the tool — the model or our code?" (Our code. Always.)
- **Watch for:** assuming the model has internet/compute. It has neither until you give it a
  tool.

### 03_agent_loop.py — the loop
- **Point:** wrap tool-calling in a `while` loop → the model chains multiple tools to finish a
  task on its own. This is a *real agent*, ~40 lines.
- **Show:** give it a task needing 2–3 tool calls; print each iteration.
- **Ask:** "What makes the loop stop? What if it never does?" (Stop = model returns a final
  answer; safeguard = max-iterations. Segue to guardrails later.)
- **Watch for:** infinite loops / no max-iteration cap — note it now, fix it in `09`.

## Day 2 AM

### 04_react_agent.py — patterns, multiple tools
- **Point:** ReAct = reason then act, repeatedly, with several tools available. Same loop,
  more tools + better prompting.
- **Ask:** "How does it decide *which* tool?" (Descriptions + the model's reasoning. Good tool
  descriptions are like good API docs.)

### 05_reflection.py — self-critique
- **Point:** a second pass where the agent grades its own output and retries — the
  evaluator-optimizer pattern. Quality up, cost up.
- **Ask:** "What did reflection cost us in tokens/latency, and was it worth it?" (Gets her
  thinking in trade-offs — the senior mindset.)

### 06_framework_agent.py — DIY vs framework
- **Point:** the same agent via the Claude Agent SDK. Frameworks remove boilerplate but hide
  the loop she now understands.
- **Ask:** "What did the framework do for us, and what did it hide?" (She can answer because
  she built the loop by hand first — that's the whole point of the ordering.)
- **Watch for:** SDK install step (uncomment in requirements.txt, reinstall).

## Day 2 PM — the ops modules (her home turf; slow down and connect to her experience)

### 07_tracing.py — observability
- **Point:** an agent is a black box without tracing. Log every step: prompt, tool I/O,
  tokens, cost, latency. *This is APM for a stochastic system.*
- **Ask:** "If this misbehaved in prod at 2am, what would you need logged?" (Let her answer
  from DevOps instinct — she'll basically derive the module.)

### 08_eval_harness.py — evals as CI
- **Point:** you can't `assert ==` on LLM output. Evals score "good enough" over a test set.
  Run them like a test suite; gate deploys on them.
- **Show:** run the harness; tweak the prompt to *break* a case and watch the score drop.
- **Ask:** "How would you wire this into CI as a merge gate?" (Bridges directly to her job.)

### 09_guardrails.py — reliability & safety
- **Point:** input/output validation, tool allow-lists, timeouts, retries, max-iterations,
  failure modes. Plus prompt injection as a new attack class.
- **Ask:** "Which of these are just IAM/WAF/timeouts you already do?" (Most of them.)

### Dockerfile + run.md — ship it
- **Point:** package the agent like any service; secrets via env, not baked in; mind rate
  limits and cost in prod.

## Capstone
- Hand her `capstone/README.md`. Her job: ship ONE small agent *with* a trace, an eval, and a
  Dockerfile. That trifecta is her first portfolio piece and the thing that gets her the
  LLMOps interview.

## Closing the weekend (15 min)
- Walk her through CAREER.md. The message: *the weekend gave her literacy; her DevOps career
  gave her the hard part. The pivot is shorter than she thinks.*
