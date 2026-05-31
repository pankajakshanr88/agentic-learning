"""
Day 1 · Lesson 02 — Tool use: giving the model hands

CONCEPT
-------
The model can't run code or hit the internet. But you can DECLARE tools to it. Then,
when it wants one, it doesn't run it — it returns a structured request: "please call
`calculator` with {expression: '23*47'}". YOUR code runs it and feeds the result back.

This single mechanism — tool/function calling — is the entire foundation of agents.

The flow for ONE tool call:
  1. You send: messages + a list of tool definitions.
  2. Model replies with stop_reason == "tool_use" and a tool_use block (name + input).
  3. You execute the tool, then send back a tool_result block.
  4. Model uses the result to write its final answer.

WHAT THIS PRINTS
----------------
  The raw tool-call request the model makes (so you SEE the JSON), then the final
  answer that uses the tool's result.

RUN
---
  python day1/02_first_tool.py
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

# --- 1. Declare the tool (this is just a schema — like API docs for the model) ---
TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression and return the number.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "An arithmetic expression, e.g. '23 * 47 + 1'.",
                }
            },
            "required": ["expression"],
        },
    }
]


# --- 2. Implement the tool in plain Python ---
def calculator(expression: str):
    # eval is fine for a toy lesson; lesson 09 covers why you'd sandbox this in prod.
    return eval(expression, {"__builtins__": {}}, {})


def main():
    messages = [{"role": "user", "content": "What is 23 * 47 + 1? Use the calculator."}]

    # First turn: the model decides to call the tool.
    resp = client.messages.create(model=MODEL, max_tokens=400, tools=TOOLS, messages=messages)
    print("stop_reason:", resp.stop_reason)  # -> 'tool_use'

    # Find the tool_use block and show the raw request.
    tool_use = next(b for b in resp.content if b.type == "tool_use")
    print(f"MODEL WANTS TO CALL: {tool_use.name}({tool_use.input})")

    # 3. WE run the tool.
    result = calculator(**tool_use.input)
    print("WE COMPUTED:", result)

    # 4. Feed the result back so the model can finish.
    messages.append({"role": "assistant", "content": resp.content})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result),
                }
            ],
        }
    )
    final = client.messages.create(model=MODEL, max_tokens=400, tools=TOOLS, messages=messages)
    print("\nMODEL FINAL:", final.content[0].text)


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Add a second tool `get_weather(city)` that just returns a hardcoded string.
#    Ask "What's 2+2 and what's the weather in Tokyo?" — watch it pick tools.
# 2. Print resp.usage after each call. Tool use costs tokens on every round-trip.
# 3. Notice: nothing here loops yet. If the model needed the calculator TWICE, this
#    code would miss the second call. That's exactly what Lesson 03 fixes.
