# Lesson Learned: AI Orchestration with Kestra

> Source: [03-orchestration](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-orchestration)  
> Module by [Will Russell](https://www.linkedin.com/in/wrussell1999/) from [Kestra](https://kestra.io/)

---

## What is Kestra?

**Kestra** is an open-source workflow orchestration platform. You define workflows declaratively in YAML, and Kestra executes them — scheduling tasks, handling retries, logging outputs, and tracking execution history — without you writing any orchestration logic yourself.

Think of it as Apache Airflow, but with:
- A built-in visual UI at `http://localhost:8080`
- Declarative YAML (no Python DAG files)
- 1000+ plugins for databases, cloud providers, APIs, and now — AI

In this module, the focus is on Kestra's AI plugins: using LLMs *inside* workflows rather than just calling them from a script.

---

## The Core Problem: Why Generic AI Fails at Workflow Generation

Before learning the solutions, it helps to understand what goes wrong without them.

**Experiment:** Ask ChatGPT (in a private window, no history) to:
> *"Create a Kestra flow that loads NYC taxi data from CSV to BigQuery."*

ChatGPT will produce YAML that looks plausible but typically contains:
- Outdated plugin type names that have been renamed
- Property names that don't exist in the current plugin API
- Hallucinated task types that were never part of Kestra

**Why?** The model only knows what was in its training data. It cannot know about plugin renames, API changes, or new best practices added after its cutoff date.

> **Key insight:** A model is only as good as the information provided to it. The solution is not a better model — it's better context.

---

## Part 1: Context Engineering

Context engineering is the practice of deliberately injecting the right information into a model's context window so it can generate accurate, useful output.

```
Without context engineering:
  User prompt  →  LLM (training data only)  →  Hallucinated / outdated output

With context engineering:
  User prompt + [current docs + plugin specs + examples]  →  LLM  →  Accurate, working output
```

The same principle applies whether you're:
- Generating Kestra flows (inject plugin documentation)
- Answering questions about your data (inject retrieved document chunks via RAG)
- Running an autonomous agent (inject tool descriptions + memory)

**Context engineering is not a trick — it is the core skill of building reliable AI applications.**

---

## Part 2: AI Copilot — Grounded Flow Generation

### What It Does

Kestra's AI Copilot is a chat interface inside the Flow Editor. Instead of writing YAML by hand, you describe your goal in natural language and the Copilot generates a working flow.

**Why it works better than ChatGPT:**  
AI Copilot injects the current Kestra plugin documentation into every request — correct type names, valid properties, and up-to-date syntax for your installed version. ChatGPT guesses. Copilot *knows*.

### The 5% Rule

Copilot gets you to a working flow in one shot. The last 5% — your specific secrets, error handling preferences, or environment-specific config — you tune manually.

### Iterative Refinement

Each follow-up prompt in Copilot preserves the existing flow and only changes what you ask for:

```
1. "Create a flow that downloads a CSV and loads it to BigQuery"
      → Copilot generates base flow

2. "Add a data quality check in BigQuery"
      → Copilot adds SQL validation tasks

3. "Schedule it daily at 9 AM UTC"
      → Copilot adds a Schedule trigger

4. "Send Slack alert on failure"
      → Copilot adds SlackIncomingWebhook in an errors branch
```

You collaborate with AI; you don't restart from scratch each time.

### Beyond the UI

If you prefer working in an editor (VS Code, Cursor, Claude Code), the [Kestra agent-skills](https://github.com/kestra-io/agent-skills) repository gives any AI coding assistant the same grounded plugin documentation — you get the same quality without leaving your editor.

---

## Part 3: RAG in Kestra — Grounding Responses in Real Data

### What RAG Solves

AI Copilot solves *flow generation*. But what about workflows that need to *answer questions* from your own documents, databases, or release notes? That's RAG.

Without RAG, an LLM asked "What features were in Kestra 1.1?" guesses from training data — it may list incorrect features, features from a different version, or features that never existed.

With RAG, the workflow first fetches the actual Kestra 1.1 release notes, embeds them, retrieves the relevant chunks, and passes them as context — producing a factually correct answer.

### How RAG Works in Kestra

RAG has two distinct phases:

```
┌─────────────────────────────────────────────────────────────────┐
│   INGEST PHASE  (run once, or on a schedule as data changes)    │
└─────────────────────────────────────────────────────────────────┘

  External doc / URL
       │
       ▼
  ┌──────────────┐
  │ IngestDocument│   io.kestra.plugin.ai.rag.IngestDocument
  │    task       │   → fetches URL, chunks text, creates embeddings
  └──────────────┘
       │
       ▼
  ┌──────────────┐
  │  KV Store    │   io.kestra.plugin.ai.embeddings.KestraKVStore
  │  (vectors)   │   → stores vector embeddings for retrieval
  └──────────────┘


┌─────────────────────────────────────────────────────────────────┐
│   QUERY PHASE  (run on demand, once per question)               │
└─────────────────────────────────────────────────────────────────┘

  User question
       │
       ▼
  ┌──────────────┐
  │ ChatCompletion│   io.kestra.plugin.ai.rag.ChatCompletion
  │  (RAG mode)  │   → embeds question, retrieves similar chunks
  └──────────────┘         from KV Store, builds augmented prompt
       │
       ▼
  ┌──────────────┐
  │  LLM Answer  │   response grounded in retrieved document chunks
  └──────────────┘
```

### Kestra Flow Example

```yaml
tasks:
  - id: ingest_release_notes
    type: io.kestra.plugin.ai.rag.IngestDocument
    provider:
      type: io.kestra.plugin.ai.provider.GoogleGemini
      modelName: gemini-embedding-001
      apiKey: "{{ secret('GEMINI_API_KEY') }}"
    embeddings:
      type: io.kestra.plugin.ai.embeddings.KestraKVStore
    drop: true
    fromExternalURLs:
      - https://raw.githubusercontent.com/kestra-io/docs/main/src/contents/blogs/release-1-1/index.md

  - id: chat_with_rag
    type: io.kestra.plugin.ai.rag.ChatCompletion
    chatProvider:
      type: io.kestra.plugin.ai.provider.GoogleGemini
      modelName: gemini-2.5-flash
      apiKey: "{{ secret('GEMINI_API_KEY') }}"
    embeddingProvider:
      type: io.kestra.plugin.ai.provider.GoogleGemini
      modelName: gemini-embedding-001
      apiKey: "{{ secret('GEMINI_API_KEY') }}"
    embeddings:
      type: io.kestra.plugin.ai.embeddings.KestraKVStore
    prompt: "Which features were released in Kestra 1.1?"
```

### Static RAG vs Web Search RAG

| | Static RAG | Web Search RAG |
|---|---|---|
| **Data source** | Documents you ingested | Live Tavily web results |
| **Freshness** | As fresh as last ingest | Real-time |
| **Ingestion step** | Required | Not required |
| **Best for** | Internal docs, policies, fixed knowledge bases | Frequently changing or time-sensitive data |
| **Quality control** | You control the source | Depends on search engine relevance |
| **Example question** | "What does our refund policy say?" | "What is the latest Kestra release?" |

> **Note on KV Store:** Kestra's KV Store is convenient for learning and small demos, but it is not a production vector database. For larger document sets or low-latency retrieval, use a dedicated vector store (see Module 2).

---

## Part 4: AI Agents — Autonomous Task Execution

### Traditional Workflow vs Agent Workflow

```
Traditional workflow — steps are predetermined:

  Task 1  →  Task 2  →  Task 3  →  Done
  (fixed sequence, always the same path)


Agent workflow — agent decides what to do based on the goal:

  Goal  →  Agent decides: "I need to search the web"
              → calls WebSearch tool
              → reads results
              → decides: "I need to search again with a different query"
              → calls WebSearch tool again
              → decides: "I have enough information"
              → produces final output
  (dynamic sequence, adapts to what it finds)
```

### The Agentic Loop (What AIAgent Does Internally)

```
┌──────────────────────────────────────────────────────┐
│                   AGENTIC LOOP                        │
│                                                        │
│  prompt + system message + tools                      │
│        │                                               │
│        ▼                                               │
│    ┌───────┐                                           │
│    │  LLM  │  ← decides: answer now, or call a tool?  │
│    └───────┘                                           │
│        │                                               │
│   ┌────┴─────────────────────────┐                    │
│   │                              │                     │
│   ▼                              ▼                     │
│  Final answer              Tool call                   │
│  (exit loop)               │                           │
│                            ▼                           │
│                       Tool executes                    │
│                       (WebSearch,                      │
│                        CodeExecution,                  │
│                        KestraTask, …)                  │
│                            │                           │
│                            ▼                           │
│                       Result fed back                  │
│                       into LLM context                 │
│                            │                           │
│                            └──► (repeat)               │
└──────────────────────────────────────────────────────┘
```

### Kestra AIAgent Plugin

```yaml
- id: research_agent
  type: io.kestra.plugin.ai.agent.AIAgent
  systemMessage: |
    You are a data analyst. Analyze data and provide insights.
  prompt: "What are the top 3 trends in this dataset?"
  provider:
    type: io.kestra.plugin.ai.provider.GoogleGemini
    modelName: gemini-2.5-flash
    apiKey: "{{ secret('GEMINI_API_KEY') }}"
  tools:
    - type: io.kestra.plugin.ai.tool.TavilyWebSearch
      apiKey: "{{ secret('TAVILY_API_KEY') }}"
```

Kestra drives the agentic loop — you just declare the goal, the tools, and the system message.

### Tools Available in Kestra

| Tool | Purpose | Example Use |
|---|---|---|
| `TavilyWebSearch` | Search the web for current information | Market research, news monitoring |
| `GoogleCustomWebSearch` | Google Custom Search API | Domain-specific web search |
| `CodeExecution` | Run code safely via Judge0 | Math calculations, data validation |
| `KestraTask` | Execute any Kestra task | Run DB queries, file operations |
| `KestraFlow` | Trigger other Kestra flows | Modular sub-workflows |
| `StreamableHttpMcpClient` | Use MCP servers via HTTP/SSE | Connect to remote MCP servers |
| `DockerMcpClient` | Use MCP servers in Docker | On-demand MCP containers |
| `AIAgent` | Use another agent as a tool | Multi-agent systems |

### Tracking Token Usage

Chain AI tasks, then log their costs:

```yaml
- id: log_token_usage
  type: io.kestra.plugin.core.log.Log
  message: |
    Multilingual Agent:
    - Input tokens:  {{ outputs.multilingual_agent.tokenUsage.inputTokenCount }}
    - Output tokens: {{ outputs.multilingual_agent.tokenUsage.outputTokenCount }}
    - Total tokens:  {{ outputs.multilingual_agent.tokenUsage.totalTokenCount }}
```

**Why this matters:** Every word in a system prompt, every output token, has a cost. Monitoring `tokenUsage` per execution is how you catch cost spikes before they become surprises.

> **Prompt precision = cost control.** Changing a summary prompt from "1 sentence" to "3 sentences" roughly triples output tokens and triples cost.

---

## Part 5: Multi-Agent Systems

For complex tasks, you compose specialized agents — each with a clear responsibility — where one agent calls another as a tool.

### Example: Company Research System

```
User input: "Research kestra.io"
        │
        ▼
┌───────────────────┐
│  Main Analyst     │  role: synthesis and structured reporting
│  Agent            │  tool: Research Agent (below)
└────────┬──────────┘
         │  calls Research Agent as a tool
         ▼
┌───────────────────┐
│  Research Agent   │  role: web data gathering
│                   │  tool: TavilyWebSearch
└────────┬──────────┘
         │  returns findings
         ▼
┌───────────────────┐
│  Main Analyst     │  synthesizes findings → structured JSON report
│  Agent            │
└───────────────────┘
```

### Why Separate Agents?

| Concern | Single Agent | Multi-Agent |
|---|---|---|
| **Separation of concerns** | Mixed responsibilities | Each agent owns one role |
| **Debugging** | Hard to isolate failures | Can pinpoint which agent failed |
| **Specialization** | One system message for everything | Optimized prompt per agent |
| **Reuse** | Coupled logic | Research agent reusable across flows |

### Pattern: `AIAgent` as a Tool

```yaml
- id: main_agent
  type: io.kestra.plugin.ai.agent.AIAgent
  prompt: "Research this company and produce a report: {{ inputs.company }}"
  tools:
    - type: io.kestra.plugin.ai.tool.AIAgent   # ← another agent as a tool
      id: research_agent
      systemMessage: "You are a web researcher. Find factual information."
      tools:
        - type: io.kestra.plugin.ai.tool.TavilyWebSearch
          apiKey: "{{ secret('TAVILY_API_KEY') }}"
```

The main agent treats the research agent exactly like a web search — it calls it when needed and acts on whatever comes back.

---

## Part 6: Best Practices

### When to Use What

| Scenario | Approach | Why |
|---|---|---|
| Generating Kestra flows | **AI Copilot** | Fastest way to get correct YAML |
| Answering questions from your data | **RAG** | Grounds responses in real documents |
| Fixed, repeatable ETL pipelines | **Traditional task-based workflow** | Deterministic, predictable, auditable |
| Research and open-ended analysis | **AI Agents** | Can adapt to findings dynamically |
| Complex multi-step objectives | **Multi-agent systems** | Specialized agents collaborating |
| Regulated / compliance workflows | **Traditional task-based workflow** | Non-determinism is a liability |

```
Is the sequence of steps known in advance?
    YES  →  Traditional task-based workflow
    NO   ↓

Does the task require adapting to dynamic findings?
    YES  →  AI Agent (with tools)
    NO   ↓

Do you need multiple specialized roles?
    YES  →  Multi-agent system
    NO   →  Single AI Agent
```

### Security — Never Commit API Keys

```yaml
# ❌ Wrong — exposed in version control
apiKey: "AIzaSy..."

# ✅ Correct — secret resolved at runtime
apiKey: "{{ secret('GEMINI_API_KEY') }}"
```

Export secrets as base64-encoded env vars before starting Kestra:
```bash
export SECRET_GEMINI_API_KEY=$(echo -n "your-key-here" | base64)
docker compose up -d
```

### Cost Considerations (Gemini API)

| Model | Tier | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|---|
| Gemini 2.5 Flash | Free | $0.00 | $0.00 |
| Gemini 2.5 Flash | Standard | $0.15 | $1.25 |
| Gemini 3.5 Flash | Standard | $1.50 | $9.00 |

**Cost-saving tips:**
1. Start on the free tier for development
2. Use smaller models (Gemini 2.5 Flash) for simple summarization tasks
3. Set `maxOutputTokens` to cap response length
4. Monitor `tokenUsage` in execution logs — output tokens are ~8× more expensive than input
5. Use traditional workflows when determinism is needed — no LLM calls means zero token cost

### Observability

Enable detailed logging for debugging agent decisions:

```yaml
- id: agent
  type: io.kestra.plugin.ai.agent.AIAgent
  configuration:
    logRequests: true
    logResponses: true
```

This surfaces: token usage per task, tool calls the agent made, request/response payloads, and execution time. Use it to understand *why* an agent took a particular path.

---

## Flow Reference Map

| Flow file | What it demonstrates |
|---|---|
| `1_chat_without_rag.yaml` | LLM answering from training data only — shows hallucination |
| `2_chat_with_rag.yaml` | Same question grounded in ingested release notes — accurate answer |
| `3_rag_with_websearch.yaml` | Live web retrieval via Tavily as a RAG source |
| `4_simple_agent.yaml` | Chained agents, controllable output length, token usage logging |
| `5_web_research_agent.yaml` | Autonomous research agent with web search tool |
| `6_multi_agent_research.yaml` | Two-agent system: research agent called by analyst agent |

---

## Key Takeaways

1. **Context is the core skill.** A model's output quality is determined by the information you give it, not just the model size. Context engineering, RAG, and grounded Copilot all apply the same principle: give the model what it needs to be right.

2. **RAG prevents hallucination.** Without retrieval, a model guesses from training data. With retrieval, it answers from facts. The two-phase pattern (ingest once → query many times) is the production pattern to know.

3. **Agents trade determinism for flexibility.** An agent loop that calls tools dynamically is powerful for open-ended tasks, but non-deterministic. Never use agents where an auditable, fixed execution path is required.

4. **Token cost scales with output length.** Prompt wording directly controls cost. "1 sentence" vs "3 sentences" is a ~3× difference in output tokens. Set `maxOutputTokens` and monitor `tokenUsage` in production.

5. **Multi-agent systems require clear role separation.** Each agent should have one responsibility, a clear system message, and access only to the tools it needs. This makes debugging easier and the system more maintainable.

6. **Traditional workflows for compliance.** Financial reporting, regulated industries, and any scenario requiring bit-for-bit reproducible results should use deterministic task-based flows — not AI agents.

7. **Secrets always go in Kestra's secret store.** Export as `SECRET_`-prefixed base64 env vars before starting Kestra. Never put API keys in YAML files committed to version control.
