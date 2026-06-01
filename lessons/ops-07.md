# 07 · Tracing: seeing into the black box

This is where the course turns toward your day job. An agent with no tracing is an unobservable
distributed system, and you already know what that costs you. The fix is the one you'd reach for
with any service: structured logs, a span per step, metrics you can aggregate. Here you wire
exactly that into the agent loop.

By the end you'll have a loop that emits one structured event per step — tokens, cost, latency,
tool input and output — and a summary you could ship straight to your log pipeline.

## The one idea

For each step, emit a structured event, the same way you'd emit a span. Capture what you'd want
at 2am: which step, which tool, the arguments and result, tokens in and out, estimated cost, and
latency. At the end, roll it up into a summary. In real life this goes to Langfuse, LangSmith,
Phoenix, or whatever you already run. The shape is the lesson; the destination is a detail.

## Reading the code

Cost attribution starts with a price per token. The exact rate will drift — update it — but the
habit of attributing dollars to each call is the point.

```python
PRICE_IN = 3.0 / 1_000_000
PRICE_OUT = 15.0 / 1_000_000
```

A tiny tracer collects events and prints each as one JSON line. That "one structured line per
event" format is what makes it greppable and pipeable into `jq`, exactly like your existing
logs.

```python
class Trace:
    def __init__(self):
        self.events = []

    def log(self, **event):
        self.events.append(event)
        print(json.dumps(event))  # one structured line per span

    def summary(self):
        cost = sum(e.get("est_cost_usd", 0) for e in self.events)
        latency = sum(e.get("latency_ms", 0) for e in self.events)
        steps = sum(1 for e in self.events if e["kind"] == "model_call")
        return {"kind": "summary", "model_calls": steps,
                "total_cost_usd": round(cost, 6), "total_latency_ms": latency}
```

Now the familiar loop, instrumented. Around each model call we time it, compute its cost from the
usage, and log a `model_call` event. Every tool call logs its own event too.

```python
t0 = time.time()
resp = client.messages.create(model=MODEL, max_tokens=600, tools=TOOLS, messages=messages)
latency_ms = int((time.time() - t0) * 1000)
cost = resp.usage.input_tokens * PRICE_IN + resp.usage.output_tokens * PRICE_OUT
tracer.log(
    kind="model_call", step=step, stop_reason=resp.stop_reason,
    input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens,
    est_cost_usd=round(cost, 6), latency_ms=latency_ms,
)
```

Run it and you get a clean event stream plus a summary line. Pipe it through `jq` and it behaves
like any structured log you've ever shipped.

## What to watch for

- Token cost is per call and it compounds across a multi-step run. The summary is where you
  notice an agent that's quietly expensive.
- Latency is per model call and it's variable. If you have an SLO, this is the number that
  threatens it.
- This is the foundation for the next two lessons. The events you log here are the dataset evals
  run against (08), and the place you'll enforce limits (09).

## Recap

- Instrument every step: tokens, cost, latency, tool input and output.
- One structured line per event keeps it greppable and pipeable.
- Summaries surface the expensive or slow runs you'd otherwise miss.
- Tracing is the base layer the eval and guardrail lessons build on.

## Your turn

1. Add a `run_id` (a UUID) to every event so you can correlate one agent run across your logs.
2. Add a cost ceiling: if cumulative `est_cost_usd` passes $0.01 mid-run, stop. You just built a
   budget guardrail — more of that in lesson 09.
3. Write the events to a `.jsonl` file and load them into pandas. That's your eval and monitoring
   dataset, and the bridge to lesson 08.
