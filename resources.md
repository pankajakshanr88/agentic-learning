# Resources

A short list, not a dump. Read the three in "this weekend" now. The rest are for the months
after, and they're sorted so you can start at the top of each section and stop when you've
had enough.

## Read these this weekend

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
  (Anthropic). The clearest writing on workflows vs. agents and the handful of patterns that
  matter. If you read one thing, read this.
- [Tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) (Anthropic).
  How function calling actually works, which is the mechanism under every lesson here.
- Andrej Karpathy's "Intro to LLMs" talk (about an hour on YouTube). The best plain
  explanation of what's inside the box.

## LLM basics

- [Build with Claude](https://docs.anthropic.com/) docs: messages, streaming, models, pricing.
- [Prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering).

## Patterns and frameworks

- Claude Agent SDK (search "Agent SDK" in the Anthropic docs).
- [LangGraph](https://langchain-ai.github.io/langgraph/), graph-based orchestration that shows
  up in a lot of job postings.
- The ReAct paper ("ReAct: Synergizing Reasoning and Acting in LLMs", Yao et al.).
- The Reflexion paper, for the self-critique loop.

## MCP

- [Model Context Protocol](https://modelcontextprotocol.io/). The server side of MCP is a
  natural specialty for someone who runs infrastructure.

## Production and LLMOps

This is the section that pays your bills, so start here for the career move.

- Eval cookbooks from Anthropic and OpenAI.
- Tracing and eval platforms: LangSmith, Langfuse, Arize Phoenix.
- The [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/),
  for prompt injection and the rest of the new attack surface.
- *AI Engineering* by Chip Huyen, the best single survey of the production stack.

## Practice

- The [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) on GitHub:
  runnable recipes for tools, RAG, and agents.

Reading is the easy part. The capstone in this repo is your first thing to actually build.
