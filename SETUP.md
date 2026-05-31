# Setup

Three things: a virtual environment, the dependencies, and an API key. You've done this kind
of thing a hundred times, so this is short.

## 1. Python environment

```bash
cd "Agentic learning"
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. API key

The scripts call the Anthropic API, so you need a key. This is the only thing in the repo
that costs money, and the lessons use small models and tiny prompts, so the whole weekend
runs to a few cents.

```bash
cp .env.example .env
```

Open `.env` and paste your key from the [Anthropic console](https://console.anthropic.com/)
(Settings → API Keys).

One thing that trips people up: an editor's AI subscription (Cursor, Copilot, whatever) is a
separate product. It does not power this Python code. The key in `.env` does.

## 3. Check it works

```bash
python day1/01_hello_llm.py
```

A reply printed from the model means you're set. If you see `ANTHROPIC_API_KEY not set`, the
`.env` isn't right. If you get an import error, the venv isn't active.

## How the lessons run

Run them in order: `day1/01 → 02 → 03`, then `day2/04 → 05 → 06`, then `day2_ops/07 → 08 →
09`. Each file opens with a short explanation of the idea, then the code, then a
`# === Your turn ===` block with a small extension. Type those yourself; that's where it
sticks.

No key in front of you right now? Each file's header says what it would print, so you can
read along and still get the idea.

## What needs what

Everything runs on two packages until Day 2's framework lesson
(`day2/06_framework_agent.py`), which needs the Claude Agent SDK. Uncomment it in
`requirements.txt` and run `pip install -r requirements.txt` again when you get there.
