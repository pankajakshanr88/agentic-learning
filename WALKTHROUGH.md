# Teaching guide

This is for whoever is leading the weekend. She follows the README; you use this. Each
module has the same four parts: the point to land, what to run, a question to check she's
got it, and what to watch for.

Pacing: Day 1 runs about 5 to 6 hours, Day 2 about 6 to 7. Break after each numbered file.
Let her type the "Your turn" blocks herself. Don't drive the keyboard the whole time.

## Before you start (10 min)

- Do the setup together and confirm `python day1/01_hello_llm.py` prints a reply.
- Land one sentence: an LLM is a stateless function, and an agent is a loop that lets it use
  tools. Everything hangs off that.

## Day 1

### 01_hello_llm.py, the function
- Point: text in, text out, no memory. The roles (system, user, assistant). Tokens are cost.
- Show: run it. Then run it again and notice it has no memory of the first call.
- Ask: if it's stateless, how does a chatbot remember your name? (You resend the history
  every call. That's the trick.)
- Watch for: thinking the model remembers. It doesn't. The caller does.

### 02_first_tool.py, giving it hands
- Point: the model can't run code. It asks your code to, with a structured tool call. Your
  code runs it and returns the result. This is the basis of every agent.
- Show: run it, and print the raw tool-call request before running it so she sees the JSON.
- Ask: who actually runs the tool, the model or our code? (Our code. Always.)
- Watch for: assuming the model has internet or compute. It has neither until you hand it a
  tool.

### 03_agent_loop.py, the loop
- Point: wrap tool-calling in a loop and the model chains tools to finish a task on its own.
  That's a real agent, in about 40 lines.
- Show: give it a task that needs two or three tool calls. Print each step.
- Ask: what stops the loop, and what if it never does? (It stops on a final answer; the
  safeguard is a max-iterations cap. That sets up guardrails later.)
- Watch for: the missing cap. Name it now; lesson 09 fixes it.

## Day 2, morning

### 04_react_agent.py, patterns and multiple tools
- Point: ReAct is reason, then act, repeated, with several tools to choose from. Same loop,
  more tools, better prompting.
- Ask: how does it pick a tool? (The descriptions, plus its reasoning. Good tool
  descriptions are good API docs.)

### 05_reflection.py, self-critique
- Point: a second pass where the agent grades its own output and retries. Quality up, cost up.
- Ask: what did reflection cost in tokens and latency, and was it worth it? (Gets her
  thinking in tradeoffs.)

### 06_framework_agent.py, by hand vs. a framework
- Point: the same agent through the Claude Agent SDK. A framework removes boilerplate and
  hides the loop she now understands.
- Ask: what did the framework do for us, and what did it hide? (She can answer, because she
  built the loop first. That's why the order matters.)
- Watch for: the SDK install step. Uncomment it in requirements.txt and reinstall.

## Day 2, afternoon (the ops modules)

This is the part closest to her day job, so slow down and keep tying it back to her experience.

### 07_tracing.py, observability
- Point: an agent is a black box without tracing. Log every step: the prompt, tool I/O,
  tokens, cost, latency. It's APM for a system that isn't deterministic.
- Ask: if this misbehaved in prod at 2am, what would you need logged? (Let her answer from
  instinct. She'll mostly derive the module.)

### 08_eval_harness.py, evals as CI
- Point: you can't assert equality on LLM output. Evals score "good enough" over a test set.
  Run them like a test suite and gate deploys on them.
- Show: run the harness. Then tweak the prompt to break a case and watch the score drop.
- Ask: how would you wire this into CI as a merge gate? (Goes straight to her job.)

### 09_guardrails.py, reliability and safety
- Point: input and output validation, tool allow-lists, timeouts, retries, a max-iterations
  cap, and a failure-mode list. Plus prompt injection as a new class of attack.
- Ask: which of these are just IAM, WAF, and timeouts you already do? (Most of them.)

### Dockerfile and run.md, shipping it
- Point: package the agent like any service. Secrets come in through the environment, not the
  image. Mind rate limits and cost in prod.

## Capstone
Hand her `capstone/README.md`. The job: ship one small agent with a trace, an eval, and a
Dockerfile. That set is her first portfolio piece and the thing that gets the interview.

## Closing (15 min)
Walk her through CAREER.md. The message: the weekend gave her literacy, and her DevOps career
already gave her the hard part. The move is shorter than she thinks.
