# 08 · Evals: tests for a system that isn't deterministic

This is the lesson where your CI instinct does the most work, and it's the skill that makes you
hireable for this. The problem is simple to state and annoying to solve: you can't write
`assert output == "expected"` for a model, because it phrases things differently every time and
can be subtly wrong. So how do you stop a prompt tweak from quietly breaking everything? You
build evals — a test set with a fuzzy pass bar — and you gate deploys on them.

By the end you'll have a runnable eval suite that scores the system three different ways and
exits non-zero on failure, so it drops straight into CI.

## The one idea

An eval is a test where "pass" means "good enough," not "equal." You collect cases, score each
one, and require the overall score to clear a threshold before you ship. There are three ways to
score, and this lesson uses all three:

- `contains` — cheap and exact, for checkable facts.
- rule-based — regex, numeric tolerance, schema checks.
- LLM-as-judge — a model grades open-ended output against a rubric.

## Reading the code

The thing under test is a small prompt we want to protect from regressions.

```python
SYSTEM = "You are a precise assistant. Answer in as few words as possible."

def system_under_test(question: str) -> str:
    resp = client.messages.create(
        model=MODEL, max_tokens=100, system=SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    return resp.content[0].text.strip()
```

The dataset is a list of cases, each carrying how to grade it. Three of these use a simple
`contains`; the last one is open-ended, so it gets a rubric for a judge.

```python
EVAL_SET = [
    {"q": "What is the capital of France?", "check": ("contains", "Paris")},
    {"q": "What is 17 * 3?", "check": ("contains", "51")},
    {"q": "Name the protocol that standardizes agent tool access (acronym).",
     "check": ("contains", "MCP")},
    {"q": "Explain idempotency to a junior engineer in one sentence.",
     "check": ("judge", "Correctly explains that repeating the operation has the same "
                        "effect as doing it once; clear; one sentence.")},
]
```

LLM-as-judge is just another model call with a tight job: read the question, answer, and rubric,
and return `PASS` or `FAIL`. It's cheap to add and surprisingly reliable for "is this good
enough" decisions.

```python
def llm_judge(question, answer, rubric) -> bool:
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
```

The part that makes it a CI gate is the ending: compute the pass rate, compare to a threshold,
and `sys.exit(1)` if it falls short. A non-zero exit is what blocks a build.

```python
if score < threshold:
    print("BELOW THRESHOLD — in CI this would FAIL the build and block deploy.")
    sys.exit(1)  # non-zero exit = CI gate
```

## What to watch for

- You're scoring "good enough," not equality. Pick the cheapest scoring method that actually
  catches the failures you care about — don't reach for a judge when `contains` will do.
- LLM-as-judge needs a tight, specific rubric. Vague rubrics give you a vague grader.
- The exit code is the whole integration story. `python 08_eval_harness.py && deploy` is your
  merge gate in one line.

## Recap

- Evals test non-deterministic output by scoring "good enough" over a test set.
- Use the right scoring method per case: contains, rule-based, or LLM-as-judge.
- Exit non-zero below threshold so it gates CI.
- Growing the eval set is the ongoing work — it's how you encode what "correct" means for you.

## Your turn

1. Break it on purpose: change `SYSTEM` to "Answer ONLY in French." Re-run and watch cases fail
   and the exit code flip. That's a regression caught before prod.
2. Add three cases from your own domain (infra Q&A, say). Growing the eval set is the real job of
   LLMOps.
3. Wire it into CI: a GitHub Action that runs this on every PR touching the prompt and blocks
   merge on exit code 1. That sentence, made real, is the LLMOps job.
