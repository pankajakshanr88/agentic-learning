"""
Day 2 · Lesson 04 — ReAct: reasoning + acting with multiple tools

CONCEPT
-------
ReAct = "Reason + Act". It's not a new mechanism — it's the SAME loop from Lesson 03,
with two upgrades:
  1. Several tools, so the model must CHOOSE which to use (good tool descriptions
     matter — they're API docs the model reads).
  2. We encourage the model to reason out loud before acting, which improves its
     tool choices.

The agent now solves an open-ended task by deciding, step by step, what to do next.

WHAT THIS PRINTS
----------------
  A trace where the model reasons, picks among a knowledge-base lookup, a calculator,
  and a clock tool, and chains them to answer a question.

RUN
---
  python day2/04_react_agent.py
"""

import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. See SETUP.md.")

from anthropic import Anthropic

client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

# A tiny fake "knowledge base" so the agent has a reason to look things up.
KB = {
    "server_count": 42,
    "cost_per_server_monthly": 30,
    "region": "us-east-1",
}

TOOLS = [
    {
        "name": "kb_lookup",
        "description": "Look up an infrastructure fact by key. Keys: server_count, "
        "cost_per_server_monthly, region.",
        "input_schema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "current_time_utc",
        "description": "Return the current UTC time as an ISO string. No arguments.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


def run_tool(name, args):
    if name == "kb_lookup":
        return KB.get(args["key"], f"no such key: {args['key']}")
    if name == "calculator":
        return eval(args["expression"], {"__builtins__": {}}, {})
    if name == "current_time_utc":
        return datetime.now(timezone.utc).isoformat(timespec="seconds")
    return f"unknown tool: {name}"


SYSTEM = (
    "You are an infrastructure assistant. Think briefly about which tool you need, then "
    "use tools to get real numbers — never guess. When you have enough, give a final answer."
)


def agent(task, max_iterations=8):
    messages = [{"role": "user", "content": task}]
    for step in range(1, max_iterations + 1):
        resp = client.messages.create(
            model=MODEL, max_tokens=700, system=SYSTEM, tools=TOOLS, messages=messages
        )
        # Show the model's reasoning (text blocks), if any.
        for block in resp.content:
            if block.type == "text" and block.text.strip():
                print(f"  [step {step}] thinking: {block.text.strip()}")

        if resp.stop_reason != "tool_use":
            return resp.content[-1].text if resp.content[-1].type == "text" else "(done)"

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                out = run_tool(block.name, block.input)
                print(f"  [step {step}] act: {block.name}({block.input}) -> {out}")
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(out)}
                )
        messages.append({"role": "user", "content": results})
    return "(stopped: hit max_iterations)"


def main():
    task = "What's our total monthly server cost, and what time is it in UTC right now?"
    print("TASK:", task, "\n")
    print("\nAGENT:", agent(task))


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Add a key 'discount_pct' = 10 to the KB and ask for cost AFTER discount. Watch
#    it look up two facts and do the math.
# 2. Worsen a tool's description (make it vague) and see tool choice get worse.
#    Tool descriptions are prompt engineering — treat them like API docs.
# 3. Ask something NONE of the tools can answer. Notice it should say so, not invent
#    a number. (If it invents one — that's a hallucination; Lesson 08 catches these.)
