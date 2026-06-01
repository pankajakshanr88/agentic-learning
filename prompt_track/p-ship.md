# Ship it — by prompt

The goal: have the agent containerize your agent, then review it the way you'd review any
service's Dockerfile, because that's exactly what it is.

## Drive

> Write a `Dockerfile` for the agent. Use a slim Python base, install from `requirements.txt`
> with layer caching, run as a non-root user, and set a default command that runs the traced
> agent. The `ANTHROPIC_API_KEY` must be passed at runtime, never baked into the image. Also
> give me the `docker build` and `docker run` commands, passing the key via `-e`.

Good output is a boring, correct Dockerfile and two commands. Boring is the goal here.

## Review

- **Is the API key kept out of the image?** Nothing secret should be `COPY`-ed or `ENV`-ed into
  the image — images get pushed to registries and shared. The key comes in at runtime via `-e`
  or a secrets manager. This is the one thing to get right.
- **Does it run as non-root?** Least privilege for the container, same as anywhere.
- **Is `requirements.txt` copied and installed before the app code?** That's the layer-caching
  habit; if it copied everything first, rebuilds will be slow.
- **The deploy reality check:** an agent run can take minutes. A blocking HTTP handler is wrong
  for that — you'd want a queue and a worker. The Dockerfile won't show this, but it's the next
  question to ask.

Push back:

> You added `ENV ANTHROPIC_API_KEY=...` to the image. Remove it — the key must only be passed at
> runtime with `-e` or a secrets manager. Also run as a non-root user.

## Understand

An agent ships like any service; the only special habits are runtime secrets and non-root.
Deep dive: [Containerizing the agent](../pages/ops-docker.html).

## Where to go now

You've driven an agent through the whole arc: model, tools, loop, patterns, framework, tracing,
evals, guardrails, and a container. The prompts gave you speed; the reviews are what make you
dangerous in the good way.

From here:
- Do the [capstone](../pages/capstone.html) — but this time, prompt your way through it and
  review hard. Ship it with a trace, an eval, and a Dockerfile.
- Read the [career roadmap](../pages/career.html). The review instinct you practiced here is the
  exact thing LLMOps hiring is looking for.
