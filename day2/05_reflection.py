"""
Day 2 · Lesson 05 — Reflection: the agent grades its own work and retries

CONCEPT
-------
"Evaluator-optimizer" pattern:
  1. A GENERATOR produces an answer.
  2. An EVALUATOR (the same model, different prompt) critiques it against criteria.
  3. If it's not good enough, feed the critique back and regenerate. Loop until it
     passes or you hit a cap.

This trades MORE tokens/latency for HIGHER quality. As a senior engineer, notice the
trade-off — reflection is not free, and you should measure whether it's worth it
(Lesson 08's evals are how you'd decide).

WHAT THIS PRINTS
----------------
  Draft 1, the critic's verdict + score, then an improved Draft 2 (and the cost of the
  extra passes).

RUN
---
  python day2/05_reflection.py
"""

import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. See SETUP.md.")

from anthropic import Anthropic

client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

total_tokens = 0


def call(system, messages, max_tokens=600):
    global total_tokens
    resp = client.messages.create(model=MODEL, max_tokens=max_tokens, system=system, messages=messages)
    total_tokens += resp.usage.input_tokens + resp.usage.output_tokens
    return resp.content[0].text


def generate(task, feedback=None):
    msg = task if not feedback else f"{task}\n\nRevise based on this feedback:\n{feedback}"
    return call("You are a technical writer. Be clear and correct.", [{"role": "user", "content": msg}])


def critique(task, draft):
    """Returns (score 1-10, feedback). The model self-evaluates against criteria."""
    system = (
        "You are a strict reviewer. Score the draft 1-10 for correctness, clarity, and "
        "completeness. Reply EXACTLY as: 'SCORE: <n>' on the first line, then bullet feedback."
    )
    out = call(system, [{"role": "user", "content": f"TASK:\n{task}\n\nDRAFT:\n{draft}"}])
    m = re.search(r"SCORE:\s*(\d+)", out)
    score = int(m.group(1)) if m else 0
    return score, out


def reflective_agent(task, threshold=8, max_rounds=3):
    draft = generate(task)
    print("DRAFT 1:\n", draft, "\n")
    for rnd in range(1, max_rounds + 1):
        score, feedback = critique(task, draft)
        print(f"--- critic round {rnd}: score {score}/10 ---")
        print(feedback, "\n")
        if score >= threshold:
            print(f"PASSED at round {rnd}.")
            return draft
        draft = generate(task, feedback)
        print(f"REVISED DRAFT (round {rnd}):\n", draft, "\n")
    print("Hit max_rounds without passing — returning best effort.")
    return draft


def main():
    task = "Explain what an agent loop is to a DevOps engineer, in 3 sentences, with one analogy."
    print("TASK:", task, "\n")
    final = reflective_agent(task)
    print("\nFINAL:\n", final)
    print(f"\n[total tokens across all passes: {total_tokens}]  <-- reflection's price")


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Set threshold=10 (hard to reach) and watch it spend all rounds + more tokens.
#    That's the quality-vs-cost knob, made visible.
# 2. Make the generator and critic use DIFFERENT models (a cheap one to write, a
#    strong one to judge). This is a common cost optimization.
# 3. Replace self-critique with a CHECKLIST the critic must verify. Deterministic
#    criteria beat vibes — and they're the seed of an eval (Lesson 08).
