# The prompt-first track

Here's the fair question behind this whole page: if agentic engineering means you *direct* an
AI to write code, why would you sit and type `client.messages.create` by hand?

You wouldn't. Not at work. At work you'd open Cursor or Windsurf, describe what you want, and
review what it builds. So this track teaches that motion directly. Every lesson leads with a
prompt you paste into your editor's agent, and the agent writes the code.

## The catch, said plainly

Prompting is the fast part. It is not the skill that gets you hired.

The skill is **reading code you didn't write and knowing whether it's right** — the same thing
you already do every day in a PR review or when an IaC plan scrolls past. An agent will happily
hand you a loop with no iteration cap, a tool with no input validation, or a confident answer
built on a number it made up. If you can't catch that, you've built a black box you can't
debug, can't explain in an interview, and can't put on call.

So every lesson here has two halves:

1. **Drive** — the prompt to paste, and what good output looks like.
2. **Review** — the specific things to check in what the agent wrote, and a follow-up prompt to
   fix what's wrong.

Each one also links to its deep-dive in the code track, where the same thing is built by hand
and explained line by line. Use that when the review checklist mentions something you want to
*understand*, not just verify.

## How to use it

Open a scratch project in Cursor or Windsurf, turn on agent mode, and have your
`ANTHROPIC_API_KEY` in a `.env` (see [Setup](../pages/setup.html)). Then go lesson by lesson:
paste the prompt, read the result against the checklist, push back where it's wrong, and only
move on once you understand what it built — not just that it ran.

Two roads, same destination. The code track teaches you what's under the hood; this track
teaches you to drive. You want both, and this one is faster.
