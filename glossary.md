# Glossary

![Interconnected nodes on a dark blue field](vendor/img/network-nodes.jpg)

Plain definitions, with the DevOps equivalent next to each one where there is a good match.
The point isn't to memorize these. It's to notice how much of "AI" vocabulary is renamed
versions of things you already run.

| Term | What it means | The thing you already know |
|------|---------------|----------------------------|
| Token | The unit a model reads and writes, roughly ¾ of a word. You pay per token. | A billable, metered usage unit |
| Context window | The most tokens a model can see at once, input plus output. | A request's payload budget; go over and you trim |
| System prompt | Standing instructions that set the agent's role and rules. | Base config applied to every request |
| Temperature | How random the output is. 0 is steady, 1 is loose. | A tunable knob; turn it down to reproduce |
| Inference | One call to the model. Text in, text out. | A single stateless request to a service |
| Tool / function calling | The model asks your code to run something; your code runs it and returns the result. | A service calling out, except the caller decides at runtime |
| Agent loop | Repeating "think, maybe call a tool, read the result" until done. | A control loop, like a Kubernetes controller |
| ReAct | A prompting pattern where the model reasons, then acts, then repeats. | A runbook run step by step with checks between |
| Reflection | The agent grades its own output and retries. | A validation gate that can trigger a redo |
| Memory | Carrying state across turns. Short-term lives in the context; long-term lives in a vector DB. | Session state vs. a persistent datastore |
| RAG | Retrieval-augmented generation: fetch relevant docs, put them in the context. | A cache/lookup layer feeding the request |
| Vector DB | Stores text as embeddings so you can search by meaning. | An index built for "find me similar things" |
| Embedding | A list of numbers that represents a piece of text's meaning. | A hash that's close for close inputs, not exact-match |
| MCP | Model Context Protocol. A standard way for agents to reach tools and data. | A driver interface like ODBC, for agent tools |
| Eval | A test that scores agent output, where "pass" is "good enough," not "equal." | A CI test with a fuzzier assertion |
| Guardrail | Limits and checks on an agent's inputs, outputs, and tool use. | Input validation, a WAF, an IAM policy, timeouts |
| Prompt injection | Text that hijacks the agent's instructions. | An injection attack, but against plain-language instructions |
| Hallucination | Output that's confident and wrong. | A 200 response with garbage in the body |
| Orchestrator-worker | One agent splits work to sub-agents and combines the results. | A scheduler handing jobs to workers |
| Evaluator-optimizer | One pass produces, another critiques, repeat until it's good. | A generate, lint, fix loop |

Missing a term? Add it as you hit it. Keeping your own glossary is half of learning a new field.
