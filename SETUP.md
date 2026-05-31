# Setup (5 minutes)

You're a senior engineer, so this is terse. Three things: a venv, the deps, a key.

## 1. Python env

```bash
cd "Agentic learning"
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. API key

The scripts call the Anthropic API. You need a key — this is the *only* thing in this repo
that costs money, and the lessons use cheap models + tiny prompts (pennies for the whole
weekend).

```bash
cp .env.example .env
```

Then open `.env` and paste your key from https://console.anthropic.com/ (Settings → API Keys).

> Note: an editor AI subscription (Cursor, Copilot, etc.) is a *separate* product and does
> **not** power this Python code. You need the key in `.env`.

## 3. Smoke test

```bash
python day1/01_hello_llm.py
```

If you see a model reply printed, you're done. If you see `ANTHROPIC_API_KEY not set`, fix
your `.env`. If you see an import error, your venv isn't activated.

## How the lessons work

- Run them in order: `day1/01 → 02 → 03`, then `day2/04 → 05 → 06`, then `day2_ops/07 → 08 → 09`.
- Every file starts with a docstring explaining the concept, then runnable code.
- Each ends with a `# === Your turn ===` block — small extensions to cement the idea.
- No API key handy right now? Each file's header notes what it would print, so reading still
  teaches the concept.

## What costs what

All lessons use small prompts. Day 2's `06_framework_agent.py` needs the Claude Agent SDK
(uncomment it in `requirements.txt` and `pip install -r requirements.txt` again when you get
there). Everything else runs on the two base packages.
