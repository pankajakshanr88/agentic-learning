"""
Day 2 · Lesson 06 — DIY vs. a framework (Claude Agent SDK)

CONCEPT
-------
You've now hand-built the agent loop three times. Frameworks exist to remove that
boilerplate: they manage the loop, tool dispatch, message history, retries, etc.

The point of this lesson is COMPARISON. You understand the loop, so you can see exactly
what the framework does for you — and what it HIDES. (Hidden control is fine until it
isn't; when something breaks in prod, the person who understands the loop wins.)

SETUP FOR THIS ONE LESSON
-------------------------
  1. Uncomment `claude-agent-sdk` in requirements.txt
  2. pip install -r requirements.txt
If the SDK isn't installed, this file prints instructions and exits cleanly — it won't
crash the rest of your weekend.

WHAT THIS PRINTS
----------------
  The same kind of multi-step answer as Lesson 04, but with ~1/3 the code, because the
  SDK runs the loop for you.

RUN
---
  python day2/06_framework_agent.py

DOCS
----
  Search the Anthropic docs for "Claude Agent SDK". The API surface evolves; if a call
  below has changed, the docs are the source of truth — adapting it is itself a good
  exercise.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. See SETUP.md.")

# Import the SDK defensively so a missing install is a friendly message, not a crash.
try:
    from claude_agent_sdk import Agent, tool  # noqa: F401
except Exception:
    sys.exit(
        "Claude Agent SDK not installed.\n"
        "  1) Uncomment 'claude-agent-sdk' in requirements.txt\n"
        "  2) pip install -r requirements.txt\n"
        "Then re-run this file. (The SDK API may differ slightly from this sketch —\n"
        "check the Anthropic 'Agent SDK' docs and adapt; that's a worthwhile exercise.)"
    )


# With the SDK, a tool is usually just a decorated Python function — the SDK reads the
# signature/docstring to build the schema you wrote by hand in Lessons 02-04.
@tool
def calculator(expression: str) -> float:
    """Evaluate a basic arithmetic expression."""
    return eval(expression, {"__builtins__": {}}, {})


@tool
def kb_lookup(key: str) -> str:
    """Look up an infra fact. Keys: server_count, cost_per_server_monthly."""
    return {"server_count": 42, "cost_per_server_monthly": 30}.get(key, "unknown key")


def main():
    # The SDK owns the loop, tool dispatch, and history — the parts you wrote by hand.
    agent = Agent(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        system="You are an infra assistant. Use tools for real numbers; never guess.",
        tools=[calculator, kb_lookup],
    )
    result = agent.run("What's our total monthly server cost?")
    print("AGENT:", result)


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Side-by-side: open day2/04_react_agent.py next to this file. List 3 things the
#    framework did that you wrote by hand, and 1 thing it now hides from you.
# 2. Add a third tool here. Notice you DON'T write an input_schema — the SDK infers it
#    from the function signature. Convenient... and one more thing abstracted away.
# 3. Decide: for the capstone, will you go DIY (full control, more code) or framework
#    (fast, less control)? Either is fine — but now it's an informed choice.
