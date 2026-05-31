"""
Day 1 · Lesson 01 — Hello, LLM: the model is a stateless function

CONCEPT
-------
An LLM does exactly one thing: text in -> text out. It has NO memory between calls,
NO internet, NO ability to run code. It just predicts the next tokens.

The three "roles" in a conversation:
  - system    : standing instructions (who the model is, the rules)
  - user      : what you say
  - assistant : what the model says back

You pay per TOKEN (~3/4 of a word), counted on both input and output. Watch usage below.

WHAT THIS PRINTS (if no API key, just read along)
-------------------------------------------------
  A one-line reply from the model, then a token count. Then a second call that proves
  the model did NOT remember the first one — because it's stateless.

RUN
---
  python day1/01_hello_llm.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()  # reads .env -> environment

# Fail friendly if the key is missing.
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key (see SETUP.md).")

from anthropic import Anthropic

client = Anthropic()  # picks up ANTHROPIC_API_KEY from the environment
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def ask(messages, system=None):
    """One inference call. `messages` is the full conversation so far."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=system or "You are a concise, friendly tutor. Answer in one or two sentences.",
        messages=messages,
    )
    text = resp.content[0].text
    usage = resp.usage  # input_tokens / output_tokens — this is what you pay for
    return text, usage


def main():
    # --- Call 1 -----------------------------------------------------------
    reply, usage = ask([{"role": "user", "content": "In one sentence, what is an LLM?"}])
    print("MODEL:", reply)
    print(f"[tokens] in={usage.input_tokens} out={usage.output_tokens}\n")

    # --- Call 2: prove it's stateless ------------------------------------
    # We DON'T send the previous turn, so the model has no idea what we asked before.
    reply2, _ = ask([{"role": "user", "content": "What did I just ask you?"}])
    print("MODEL (fresh call, no history):", reply2)
    print("\nSee? It can't know — each call is independent. Memory is the CALLER's job.")


if __name__ == "__main__":
    main()


# === Your turn ===============================================================
# 1. Make it remember: build a list `history`, append each user + assistant turn,
#    and pass the whole list to ask(). Now ask "what did I just ask you?" again.
#    -> You just implemented short-term memory. It's just resending the transcript.
# 2. Change the `system` prompt to make the tutor answer like a grumpy sysadmin.
#    Notice the system prompt steers behavior without changing the user message.
# 3. Lower max_tokens to 10 and watch the reply get cut off. Tokens = budget.
