# Agentic Engineering — A Weekend Intensive (for a Senior DevOps Engineer)

You already know how to ship, observe, and operate systems. This weekend you learn the one
component you haven't operated yet: a **non-deterministic, tool-using LLM agent**. The good
news — the *hard* part of production agents (deploy, trace, eval, guardrail, cost-control) is
DevOps with the labels changed. You're closer to this job than almost anyone.

> **Goal of the weekend:** go from "what is an agent" to *three working agents + an ops-grade
> harness* you built and understand line-by-line. This is Phase 1 of a career pivot, not the
> whole thing — see [CAREER.md](CAREER.md) for the road after.

## Start here

1. Read this page (5 min).
2. Do [SETUP.md](SETUP.md) (5 min).
3. Work the lessons in order. Each is a runnable file; the code is the lesson.

> **Prefer one rich page?** Double-click **`index.html`** — a self-contained, offline
> single-page version of this whole repo with a sidebar, search, syntax-highlighted lessons,
> dark/light toggle, copy buttons, and a progress tracker that remembers what you've done.
> (No internet needed; regenerate after editing any doc with `python build_site.py`.)

## The mental model (read before Day 1)

**An LLM is a stateless function:** text in → text out. No memory, no actions, just
prediction. By itself it's a very smart autocomplete.

**An agent is a loop around that function** that lets it *act*:

```
            ┌──────────────────────────────────────────┐
            │                                            │
   goal ──▶ │  LLM decides: answer, or call a tool?      │
            │      │                                     │
            │      ├─ tool call ─▶ you run the tool ─────┤  (result fed back in)
            │      │                                     │
            │      └─ final answer ─▶ done               │
            │                                            │
            └──────────────────────────────────────────┘
```

That's it. The whole field is variations on: *what tools, what loop, how much autonomy, and
how do you keep it reliable.* Two terms you'll see everywhere (Anthropic's "Building Effective
Agents" framing):

- **Workflow** — *you* hard-code the steps; the LLM fills in the blanks. Predictable.
- **Agent** — the *LLM* decides the steps at runtime. Flexible, harder to control.

Most production "agents" are mostly workflows with a few agentic steps. Reliability lives on
that spectrum.

## The schedule

| When | Files | You'll be able to… |
|------|-------|--------------------|
| **Day 1** | `day1/01–03` | Explain LLMs/tools/the loop; hand-build a real agent |
| **Day 2 AM** | `day2/04–06` | Use ReAct, reflection, and a real framework (Claude Agent SDK) |
| **Day 2 PM** | `day2_ops/07–09` + Dockerfile | Trace, eval-as-CI, guardrail, and containerize an agent |
| **Capstone** | `capstone/` | Ship one ops-flavored agent *with* tracing + an eval + Docker |

Supporting docs: [glossary.md](glossary.md) (terms ↔ DevOps analogies),
[resources.md](resources.md) (the canon), [CAREER.md](CAREER.md) (the pivot roadmap).
Teaching this to someone? [WALKTHROUGH.md](WALKTHROUGH.md) is the facilitator guide.

## Why your DevOps background is the cheat code

| What employers struggle to find | What you already do |
|---|---|
| Agents that are observable in prod | APM, tracing, structured logging |
| Catching regressions in a stochastic system | CI gates, test suites → **evals** |
| Cost & latency under control | Resource budgeting, rate limiting |
| Safe tool access, secrets, sandboxing | IAM, least-privilege, container isolation |
| Reliable deploys & rollback of prompts/models | Versioning, blue/green, canaries |

You're not starting over. You're adding one new primitive to a toolkit you already have.
