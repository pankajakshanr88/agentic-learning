"""
Day 2 · Lesson 08 (OPS) — Evals: tests for a non-deterministic system

THE MOST IMPORTANT OPS LESSON. This is where your CI/CD instinct becomes your edge.

THE PROBLEM
-----------
You can't `assert output == "expected"` on an LLM — it phrases things differently every
time, and it can be subtly wrong. So how do you stop a prompt change from silently
breaking things? EVALS: a dataset of cases + a scorer that decides "good enough",
run like a test suite, used as a CI GATE before you ship a prompt/model change.

THREE SCORING STYLES (this file shows all three):
  - exact/contains  : cheap, deterministic, for checkable facts
  - rule-based      : regex / numeric tolerance / schema checks
  - LLM-as-judge    : a model grades against a rubric (for open-ended output)

WHAT THIS PRINTS
----------------
  A pass/fail line per case and an overall score. Exit code is non-zero if below the
  threshold — so you can drop this straight into CI (`python 08_eval_harness.py && deploy`).

RUN
---
  python day2_ops/08_eval_harness.py
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

# --- The system under test: a tiny agent/prompt we want to protect from regressions ---
SYSTEM = "You are a precise assistant. Answer in as few words as possible."


def system_under_test(question: str) -> str:
    resp = client.messages.create(
        model=MODEL, max_tokens=100, system=SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    return resp.content[0].text.strip()


# --- The eval dataset: input + how to grade it ---
# 'check' is how we score this case. Three styles shown.
EVAL_SET = [
    {"q": "What is the capital of France?", "check": ("contains", "Paris")},
    {"q": "What is 17 * 3?", "check": ("contains", "51")},
    {"q": "Name the protocol that standardizes agent tool access (acronym).",
     "check": ("contains", "MCP")},
    {"q": "Explain idempotency to a junior engineer in one sentence.",
     "check": ("judge", "Correctly explains that repeating the operation has the same "
                        "effect as doing it once; clear; one sentence.")},
]


def llm_judge(question, answer, rubric) -> bool:
    """LLM-as-judge: a model scores open-ended output against a rubric. Cheap to add,
    surprisingly reliable for 'is this good enough' decisions."""
    judge_system = (
        "You are a grader. Given a QUESTION, an ANSWER, and a RUBRIC, reply with exactly "
        "'PASS' or 'FAIL' on the first line."
    )
    out = client.messages.create(
        model=MODEL, max_tokens=10, system=judge_system,
        messages=[{"role": "user",
                   "content": f"QUESTION: {question}\nANSWER: {answer}\nRUBRIC: {rubric}"}],
    ).content[0].text.strip().upper()
    return out.startswith("PASS")


def score_case(case) -> bool:
    answer = system_under_test(case["q"])
    kind, expected = case["check"]
    if kind == "contains":
        passed = expected.lower() in answer.lower()
    elif kind == "judge":
        passed = llm_judge(case["q"], answer, expected)
    else:
        passed = False
    mark = "PASS" if passed else "FAIL"
    print(f"  [{mark}] {case['q']}\n         -> {answer!r}")
    return passed


def main(threshold=0.75):
    print("Running eval suite...\n")
    results = [score_case(c) for c in EVAL_SET]
    score = sum(results) / len(results)
    print(f"\nSCORE: {score:.0%}  ({sum(results)}/{len(results)} passed)  threshold={threshold:.0%}")

    if score < threshold:
        print("BELOW THRESHOLD — in CI this would FAIL the build and block deploy.")
        sys.exit(1)  # non-zero exit = CI gate
    print("PASSED — safe to ship this prompt/model.")


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Break it on purpose: change SYSTEM to "Answer ONLY in French." Re-run — watch
#    cases fail and the exit code flip. That's a regression caught before prod.
# 2. Add 3 cases that matter to YOUR domain (e.g., infra Q&A). Growing the eval set is
#    the real ongoing work of LLMOps.
# 3. Wire it into CI: a GitHub Action that runs this on every PR touching the prompt,
#    and blocks merge on exit code 1. THAT is the LLMOps job in one sentence.
