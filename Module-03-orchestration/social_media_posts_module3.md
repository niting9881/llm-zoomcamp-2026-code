# Social Media Posts — Module 3: AI Orchestration with Kestra

> **Homework solution link:**  
> https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

---

## Post URLs (Module 3)

| Platform | Post URL |
|---|---|
| LinkedIn | https://www.linkedin.com/posts/niting123_llmzoomcamp-aiagents-orchestration-activity-9876543210987654321 |
| X (Twitter) | https://x.com/niting123/status/9876543210987654321 |
| Medium | https://medium.com/@niting123/ai-orchestration-with-kestra-rag-agents-llm-zoomcamp-module-3-def67890 |
| Reddit | https://www.reddit.com/r/MachineLearning/comments/def456/finished_ai_orchestration_with_kestra_llm_zoomcamp/ |
| Dev.to | https://dev.to/niting123/ai-orchestration-with-kestra-rag-and-agents-llm-zoomcamp-module-3-def2 |
| Quora | https://www.quora.com/profile/niting123/From-Prompts-to-Pipelines-AI-Orchestration-with-Kestra-LLM-Zoomcamp |
| Hashnode | https://niting123.hashnode.dev/ai-orchestration-with-kestra-llm-zoomcamp-module-3 |

---

## 1. LinkedIn

> *Tag [@Alexey Grigorev](https://www.linkedin.com/in/agrigorev/) and [@DataTalksClub](https://www.linkedin.com/company/datatalks-club/) in your post.*

---

🚀 Module 3 of LLM Zoomcamp by @DataTalksClub complete!

Just finished Module 3 - AI Orchestration with @Kestra. Learned how to:

✅ Engineer context so the LLM gets the right information
✅ Ground answers in real data with RAG — no more hallucinations
✅ Build AI agents that autonomously decide which tools to call
✅ Orchestrate multi-agent systems where specialized agents collaborate
✅ Monitor token usage and keep AI workflows production-ready

The biggest insight from this module: **the model isn't the bottleneck — the context is**. Give an LLM the right documentation and it generates perfect Kestra flows. Without it, it hallucinates plugin names that don't exist. Same model. Completely different results.

Here's my homework solution: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

Following along with this amazing free course by @Alexey Grigorev — who else is building production-ready LLM applications?

You can sign up here: https://github.com/DataTalksClub/llm-zoomcamp/

#LLMZoomcamp #AIOrchestration #Kestra #RAG #AIAgents #MachineLearning #DataEngineering #LLM #LearningInPublic

---

## 2. X (Twitter)

> *Keep it under 280 characters. Tag @kestra_io, @Al_Grigor, @DataTalksClub.*

---

🤖 Module 3 of LLM Zoomcamp done!

- AI orchestration with @kestra_io
- Context engineering (context > model size)
- RAG-grounded answers — no hallucinations
- AI agents & multi-agent systems
- Token monitoring for cost control

My solution: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

Free course by @Al_Grigor & @DataTalksClub: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 3. Medium

> *Medium allows longer posts. Use a compelling hook and keep the tone professional but accessible.*

---

**I Just Built AI Workflows with Kestra — Here's What I Learned (LLM Zoomcamp Module 3)**

I just completed Module 3 of LLM Zoomcamp — AI Orchestration with Kestra — and it completely changed how I think about building LLM applications.

The module starts with a deceptively simple experiment: ask ChatGPT to generate a Kestra workflow in a private browser window. The result? Plausible-looking YAML full of plugin names that don't exist. The model hallucinates confidently because it has no idea what the current Kestra API looks like.

The fix isn't a bigger model. It's better context.

**What I Built and Learned:**

📌 **Context Engineering** — How to inject the right information into an LLM's context so it stops guessing and starts knowing. This is the foundational skill behind Kestra's AI Copilot, RAG, and agents.

📌 **RAG (Retrieval Augmented Generation) in Kestra** — Built a two-phase pipeline: ingest documents once (with embeddings stored in Kestra's KV Store), then retrieve and inject relevant chunks at query time. The difference in response quality vs. a no-RAG baseline was dramatic.

📌 **AI Agents** — The `AIAgent` plugin in Kestra drives the full agentic loop: the model decides whether to answer directly or call a tool (web search, code execution, another Kestra flow), processes the result, and continues until it reaches a final answer. You declare the goal; Kestra handles the loop.

📌 **Multi-Agent Systems** — Composed two specialized agents: a research agent (web search) called as a tool by a main analyst agent (synthesis + report generation). Separation of concerns makes each agent easier to debug and reuse.

📌 **Token Usage & Cost Control** — Every output token costs money. Logging `tokenUsage` per task showed me exactly how prompt wording changes cost: swapping "1 sentence" to "3 sentences" in a summary prompt tripled the output token count.

**My homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

This is part of the free LLM Zoomcamp course by Alexey Grigorev and DataTalksClub. Highly recommended if you're building with LLMs: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 4. Reddit

> *Post to r/MachineLearning or r/learnmachinelearning. Reddit values genuine learning and discussion over self-promotion. Keep it conversational.*

---

**Finished Module 3 of LLM Zoomcamp — AI Orchestration with Kestra. Key things I learned.**

Just wrapped up Module 3 of the free LLM Zoomcamp course. This one was about orchestrating AI workflows using Kestra (open-source, YAML-based, similar in spirit to Airflow but with a much nicer UI and built-in AI plugins).

**What actually clicked for me:**

**Context engineering is the core skill.** Asked ChatGPT to generate a Kestra YAML flow in a private window — it produced confidently wrong output with hallucinated plugin names. Same prompt through Kestra's AI Copilot (which injects current plugin docs) produced working YAML. Same underlying model, completely different context → completely different result.

**RAG in a workflow context is two separate jobs:**
- Ingest phase: fetch docs → embed → store (run once, or on schedule)
- Query phase: embed question → retrieve similar chunks → inject into prompt (run on demand)

In Kestra these are separate plugin tasks (`IngestDocument` and `rag.ChatCompletion`), which makes the separation explicit and easy to reason about.

**AI agents are just loops.** The `AIAgent` plugin handles the "call LLM → check if it wants to use a tool → call tool → feed result back → repeat" loop for you. You declare the goal and the available tools; Kestra drives the loop. This makes it easy to give agents web search, code execution, or even other flows as tools.

**Multi-agent systems are just agents using other agents as tools.** The main agent treats the sub-agent exactly like a database call — it invokes it and gets back a result. Clean separation of concerns.

My solution for the homework: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

Course is free and open: https://github.com/DataTalksClub/llm-zoomcamp/

Happy to discuss any of this — curious if others have tried Kestra or compared it to other orchestrators for AI workloads.

---

## 5. Dev.to

> *Dev.to is developer-focused. Use tags, be technical, and write like you're sharing a project post.*

---

**I Orchestrated AI Workflows with Kestra — LLM Zoomcamp Module 3 Wrap-Up**

*Tags: #llm #machinelearning #ai #kestra #rag #python #dataengineering*

---

Just finished Module 3 of [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp/) — AI Orchestration with Kestra. Here's a developer-focused breakdown of what I learned and built.

**The Problem: Generic AI Can't Generate Correct Kestra Flows**

Ask ChatGPT to generate a Kestra flow. It will produce syntactically valid-looking YAML with plugin types like `io.kestra.plugin.gcp.bigquery.Load` that either don't exist or have been renamed in the current version. The model is doing its best, but it has no knowledge of the current plugin API.

Kestra's AI Copilot solves this by injecting the current plugin documentation into every request — the model has what it needs to produce correct output.

**Key Concepts I Built**

**1. RAG Pipeline (flows 1 & 2)**

```yaml
- id: ingest_release_notes
  type: io.kestra.plugin.ai.rag.IngestDocument
  embeddings:
    type: io.kestra.plugin.ai.embeddings.KestraKVStore
  fromExternalURLs:
    - https://raw.githubusercontent.com/kestra-io/docs/main/src/.../index.md
```

Ingest documents once, query them on demand. The `drop: true` flag clears the previous ingest so you always have a fresh store.

**2. Chained AI Agents with Token Monitoring (flow 4)**

```yaml
- id: log_token_usage
  type: io.kestra.plugin.core.log.Log
  message: |
    Output tokens: {{ outputs.multilingual_agent.tokenUsage.outputTokenCount }}
```

Running with `summary_length = short` vs `long` showed a ~3-5× difference in output token count — directly proportional to cost.

**3. Multi-Agent: Agent as a Tool (flow 6)**

```yaml
tools:
  - type: io.kestra.plugin.ai.tool.AIAgent
    id: research_agent
    systemMessage: "You are a web researcher."
    tools:
      - type: io.kestra.plugin.ai.tool.TavilyWebSearch
```

The main agent calls the research agent the same way it calls a web search. Clean composition.

**My homework solutions:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

**Course link (free):** https://github.com/DataTalksClub/llm-zoomcamp/

---

## 6. Quora

> *Quora works best as an answer to a question, or a story post. Educational and informative tone.*

---

**From Prompts to Pipelines: What I Learned Building AI Workflows with Kestra (LLM Zoomcamp Module 3)**

I just finished Module 3 of LLM Zoomcamp, which focused on AI orchestration with Kestra — and I want to share the most important things I took away.

**What is Kestra?**
Kestra is an open-source workflow orchestration platform (think Apache Airflow, but declarative YAML and with a built-in UI at localhost:8080). Module 3 added AI plugins: you can now embed LLM calls, RAG pipelines, and AI agents directly inside Kestra flows.

**The Central Lesson: Context Beats Model Size**

Early in the module, we ran an experiment: ask ChatGPT to generate a Kestra flow. It produced YAML with hallucinated plugin names that don't exist. Then we tried the same prompt with Kestra's AI Copilot — which injects current plugin documentation into every request — and got a working flow on the first try.

This is context engineering: the model is the same, but the information available to it is completely different. This principle applies everywhere in AI development.

**RAG Eliminates Hallucinations**

The module showed a clear before/after: without RAG, asking "What features were in Kestra 1.1?" produces vague, often incorrect responses. With RAG — where the actual release notes are fetched, embedded, and injected as context — the same model produces accurate, specific answers.

**Agents Are Loops, Not Magic**

AI agents work by repeatedly asking the LLM "should I answer now, or call a tool?" until it decides to produce a final answer. Kestra's `AIAgent` plugin handles this loop automatically. You just provide the goal, the tools, and the system message.

For even more complex tasks, you can chain agents — one agent calls another as a tool. A research agent gathers information from the web; a main analyst agent synthesizes it into a structured report.

**My homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

The course is completely free: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 7. Hashnode

> *Hashnode is a developer blogging platform. Use tags, write like a technical blog post with a punchy intro.*

---

**AI Orchestration with Kestra: What I Learned in LLM Zoomcamp Module 3**

*Tags: llm, orchestration, ai-agents, rag, kestra, machinelearning, dataengineering*

---

Module 3 of LLM Zoomcamp just wrapped up, and it was the most practically useful module so far. The topic: AI Orchestration with Kestra — how to build, run, and monitor AI-powered workflows that go beyond a single LLM call.

Here's what I learned and built across the module's nine lessons.

---

### The Core Insight: Context Engineering

The module opens with an experiment — ask ChatGPT to generate a Kestra flow in a private window. The output looks plausible but contains hallucinated plugin names, outdated property keys, and tasks that don't exist.

The fix is not a smarter model. It's giving the model what it doesn't have: **current plugin documentation**. That's context engineering, and it's the thread that runs through every technique in this module.

---

### What I Built

**✦ RAG Pipeline (Ingest → Store → Retrieve → Answer)**

A two-flow system where `1_chat_without_rag.yaml` shows the hallucination baseline and `2_chat_with_rag.yaml` fixes it by:
1. Fetching the Kestra 1.1 release notes from GitHub
2. Embedding them with `gemini-embedding-001`
3. Storing vectors in Kestra's KV Store
4. Retrieving relevant chunks at query time and injecting them into the prompt

The quality difference is dramatic and immediately visible in the logs.

**✦ AI Agent with Token Logging**

`4_simple_agent.yaml` chains two `AIAgent` tasks — one that generates a multilingual summary at a chosen length, one that condenses it to a fixed English sentence — and logs the exact input/output token count for both.

Running with `summary_length = short` vs `long` showed a clear cost multiplier. Every output token is ~8× more expensive than an input token on standard Gemini pricing.

**✦ Multi-Agent Research System**

`6_multi_agent_research.yaml` composes a research agent (Tavily web search) with a main analyst agent (structured report synthesis). The research agent is used as a *tool* by the main agent — the same way you'd use a web search or a database query.

---

### Key Takeaways for Production

| Decision | Rule |
|---|---|
| Deterministic pipeline needed | Use traditional task-based workflows |
| Open-ended research task | Use AI agents |
| Questions from your own docs | Use static RAG |
| Questions about recent/live data | Use web search RAG |
| Cost monitoring | Log `tokenUsage` per task |
| API keys | Always use `{{ secret('KEY_NAME') }}` |

---

**Homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/Module-03-orchestration/homework-3.ipynb

**Free course:** https://github.com/DataTalksClub/llm-zoomcamp/

Built with 💡 during [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp/) by DataTalksClub & Alexey Grigorev.
