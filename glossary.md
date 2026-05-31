# Glossary — LLM/agent terms mapped to what you already know

Plain definitions, with a DevOps analogy where one helps.

| Term | What it means | DevOps analogy |
|---|---|---|
| **Token** | The unit an LLM reads/writes (~¾ of a word). You pay per token. | A billable request unit / metered usage. |
| **Context window** | Max tokens the model can "see" at once (input + output). | A request's payload size budget — exceed it and you must trim. |
| **System prompt** | Standing instructions that set the agent's role/rules. | Base config / environment defaults applied to every request. |
| **Temperature** | Randomness of output (0 = deterministic-ish, 1 = creative). | A tunable knob; turn it down for reproducibility. |
| **Inference** | One call to the model (text in → text out). | A single stateless HTTP request to a service. |
| **Tool / function calling** | The model emits a structured request to run code; you run it and feed back the result. | A service calling out to another API — except the *caller* decides at runtime. |
| **Agent loop** | Repeating "think → maybe call a tool → observe result" until done. | A control loop / reconciliation loop (think Kubernetes controller). |
| **ReAct** | Prompting pattern: model interleaves Reasoning and Acting (tool calls). | Run book executed step-by-step with checks between steps. |
| **Reflection** | Agent critiques/grades its own output and retries. | A post-step validation gate that can trigger a redo. |
| **Memory** | Carrying state across turns: short-term (in context) or long-term (a vector DB). | Session state vs. a persistent datastore. |
| **RAG** | Retrieval-Augmented Generation: fetch relevant docs, stuff them into context. | Cache/lookup layer feeding the request with fresh data. |
| **Vector DB** | Stores text as embeddings for similarity search. | A specialized index for "find me semantically similar things." |
| **Embedding** | A numeric vector representing text meaning. | A hash that's *similar* for *similar* inputs (not exact-match). |
| **MCP** | Model Context Protocol — a standard so agents connect to tools/data uniformly. | A standard protocol/driver interface (like ODBC) for agent tools. |
| **Eval** | A test that scores agent output (often non-binary). | A test in CI — but the assertion is "good enough," not "==". |
| **Guardrail** | Validation/limits on agent inputs, outputs, and tool use. | Input validation + WAF + IAM policy + timeouts, for an LLM. |
| **Prompt injection** | Malicious text that hijacks the agent's instructions. | Injection attack (think SQLi) but against natural-language instructions. |
| **Hallucination** | Confident, wrong output. | A service returning a 200 with garbage in the body. |
| **Token cost / latency** | $ and time per call; both scale with tokens. | Cloud spend + p99 latency you have to budget and monitor. |
| **Orchestrator-worker** | One agent splits work to sub-agents and combines results. | A scheduler dispatching jobs to workers. |
| **Evaluator-optimizer** | One agent produces, another critiques, loop until good. | Generate → lint → fix loop. |

If a term isn't here, add it as you learn it — keeping your own glossary is half the battle.
