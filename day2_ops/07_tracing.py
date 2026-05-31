"""
Day 2 · Lesson 07 (OPS) — Tracing: making the black box observable

THIS IS YOUR HOME TURF.
An agent without tracing is an unobservable distributed system. You already know the
fix: structured logs + spans + metrics. Here we instrument every step of the agent loop
with exactly that — prompt, tool I/O, tokens, cost, latency.

CONCEPT
-------
For each step we emit a structured event (think: one span):
  step, tool, args, result, input_tokens, output_tokens, est_cost_usd, latency_ms
At the end we print a summary (total cost, total latency, step count) — the stuff you'd
ship to Langfuse/LangSmith/Phoenix or your existing log pipeline in real life.

WHAT THIS PRINTS
----------------
  A JSON trace line per step, then a run summary. Pipe it to `jq` like any structured log.

RUN
---
  python day2_ops/07_tracing.py
  python day2_ops/07_tracing.py | jq    # if you have jq, see the structured events
"""

import json
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. See SETUP.md.")

from anthropic import Anthropic

client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

# Rough public pricing (USD per token). Update to current rates — the POINT is that you
# attribute cost per step, not the exact number.
PRICE_IN = 3.0 / 1_000_000
PRICE_OUT = 15.0 / 1_000_000

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    }
]


def run_tool(name, args):
    if name == "calculator":
        return eval(args["expression"], {"__builtins__": {}}, {})
    return "unknown tool"


class Trace:
    """Minimal tracer. In prod this is your logger / OTel exporter / Langfuse client."""

    def __init__(self):
        self.events = []

    def log(self, **event):
        self.events.append(event)
        print(json.dumps(event))  # one structured line per span

    def summary(self):
        cost = sum(e.get("est_cost_usd", 0) for e in self.events)
        latency = sum(e.get("latency_ms", 0) for e in self.events)
        steps = sum(1 for e in self.events if e["kind"] == "model_call")
        return {"kind": "summary", "model_calls": steps,
                "total_cost_usd": round(cost, 6), "total_latency_ms": latency}


def agent(task, tracer, max_iterations=6):
    messages = [{"role": "user", "content": task}]
    for step in range(1, max_iterations + 1):
        t0 = time.time()
        resp = client.messages.create(model=MODEL, max_tokens=600, tools=TOOLS, messages=messages)
        latency_ms = int((time.time() - t0) * 1000)
        cost = resp.usage.input_tokens * PRICE_IN + resp.usage.output_tokens * PRICE_OUT
        tracer.log(
            kind="model_call", step=step, stop_reason=resp.stop_reason,
            input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens,
            est_cost_usd=round(cost, 6), latency_ms=latency_ms,
        )

        if resp.stop_reason != "tool_use":
            return resp.content[0].text

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                out = run_tool(block.name, block.input)
                tracer.log(kind="tool_call", step=step, tool=block.name,
                           args=block.input, result=str(out))
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(out)})
        messages.append({"role": "user", "content": results})
    return "(stopped: max_iterations)"


def main():
    tracer = Trace()
    answer = agent("Compute (12*8) + (100/4). Show the result.", tracer)
    print(json.dumps(tracer.summary()))
    print("\nAGENT:", answer)


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Add a run_id (uuid) to every event so you can correlate one agent run in logs.
# 2. Add a cost CEILING: if cumulative est_cost_usd exceeds $0.01 mid-run, stop. You
#    just built a budget guardrail (more in Lesson 09).
# 3. Write the events to a .jsonl file and load them into pandas. That's your eval +
#    monitoring dataset — the bridge to Lesson 08.
