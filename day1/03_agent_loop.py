"""
Day 1 · Lesson 03 — The agent loop: this is a real agent

CONCEPT
-------
Lesson 02 handled ONE tool call. An agent handles as many as the task needs, by
LOOPING:

    while True:
        ask the model
        if it returned a final answer:  break
        else (it called tools):         run them, feed results back, loop again

That's the whole idea. ~40 lines below is a genuine, autonomous, multi-step agent.
Everything fancier (ReAct, reflection, multi-agent) is a variation on this loop.

Note the `max_iterations` cap — without it, a confused agent could loop forever.
Hold that thought; Lesson 09 turns it into a proper guardrail.

WHAT THIS PRINTS
----------------
  A trace of each iteration: which tool the model called, the result, and finally the
  answer — for a task that needs SEVERAL tool calls in sequence.

RUN
---
  python day1/03_agent_loop.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. See SETUP.md.")

from anthropic import Anthropic

client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

# --- Two tools so the model has to chain calls ---
TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "word_count",
        "description": "Count the words in a piece of text.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
]


def run_tool(name, args):
    if name == "calculator":
        return eval(args["expression"], {"__builtins__": {}}, {})
    if name == "word_count":
        return len(args["text"].split())
    return f"unknown tool: {name}"


def agent(task: str, max_iterations: int = 6):
    messages = [{"role": "user", "content": task}]

    for step in range(1, max_iterations + 1):
        resp = client.messages.create(model=MODEL, max_tokens=600, tools=TOOLS, messages=messages)

        # Did it finish?
        if resp.stop_reason != "tool_use":
            return resp.content[0].text

        # Otherwise: run every tool it asked for, collect results.
        messages.append({"role": "assistant", "content": resp.content})
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                out = run_tool(block.name, block.input)
                print(f"  [step {step}] {block.name}({block.input}) -> {out}")
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(out)}
                )
        messages.append({"role": "user", "content": tool_results})

    return "(stopped: hit max_iterations — the agent didn't converge)"


def main():
    task = (
        "First compute 144 / 12. Then count the words in the sentence "
        "'agents are just loops around a model'. Tell me both answers."
    )
    print("TASK:", task, "\n")
    answer = agent(task)
    print("\nAGENT:", answer)


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Add a `reverse_string(text)` tool and ask a 3-step task. Watch it chain 3 calls.
# 2. Set max_iterations=1 and give it a 2-step task — see it fail to converge. That's
#    why the cap matters (and why observability in Lesson 07 matters).
# 3. Add a print of the model's reasoning text (blocks where block.type == 'text')
#    BEFORE the tool calls — that's the "thinking out loud" you'll formalize as ReAct.
