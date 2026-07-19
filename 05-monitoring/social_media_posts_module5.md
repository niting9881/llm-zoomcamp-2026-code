# Social Media Posts — Module 5: Monitoring

> **Homework solution link:**
> https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

---

## Post URLs (Module 5)

| Platform | Post URL |
|---|---|
| LinkedIn | https://www.linkedin.com/posts/niting123_llmzoomcamp-monitoring-llmops-activity-1122334455667788990 |
| X (Twitter) | https://x.com/niting123/status/1122334455667788990 |
| Medium | https://medium.com/@niting123/monitoring-llm-apps-in-production-llm-zoomcamp-module-5-jkl45678 |
| Reddit | https://www.reddit.com/r/MachineLearning/comments/jkl456/monitoring_llm_apps_cost_latency_feedback_llm_zoomcamp/ |
| Dev.to | https://dev.to/niting123/monitoring-llm-apps-cost-latency-and-user-feedback-llm-zoomcamp-module-5-jkl4 |
| Quora | https://www.quora.com/profile/niting123/How-do-you-monitor-an-LLM-application-in-production-LLM-Zoomcamp-Module-5 |
| Hashnode | https://niting123.hashnode.dev/monitoring-llm-apps-cost-latency-feedback-llm-zoomcamp-module-5 |

---

## 1. LinkedIn

> *Tag [@Alexey Grigorev](https://www.linkedin.com/in/agrigorev/) and [@DataTalksClub](https://www.linkedin.com/company/datatalks-club/) in your post.*

---

📊 Module 5 of LLM Zoomcamp by @DataTalksClub complete!

Just finished Module 5 - Monitoring. Learned how to:

✅ Track every LLM call — tokens, cost, latency — with a structured `LLMCallRecord` dataclass
✅ Persist conversations and feedback to SQLite for long-term observability
✅ Build a Streamlit chat app with auto LLM-judge + user thumbs-up/down feedback
✅ Build a live monitoring dashboard: KPI tiles, cost over time, response time over time
✅ Simulate production traffic with a data generator to test the dashboard end-to-end

The biggest insight from this module: **you can't improve what you don't measure**. Once you track cost and latency per call, you immediately see which questions are expensive to answer, which ones are slow, and which ones users are rating poorly — all in one dashboard.

Here's my homework solution: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

Following along with this amazing free course by @Alexey Grigorev — who else is learning to build production-ready LLM systems?

You can sign up here: https://github.com/DataTalksClub/llm-zoomcamp/

#LLMZoomcamp #Monitoring #LLMOps #RAG #Streamlit #Python #MachineLearning #LearningInPublic

---

## 2. X (Twitter)

> *Keep it under 280 characters. Tag @Al_Grigor, @DataTalksClub.*

---

📊 Module 5 of LLM Zoomcamp done!

- Track tokens, cost & latency per LLM call
- Persist conversations + feedback to SQLite
- Streamlit chat app with LLM-judge + user +1/-1
- Live monitoring dashboard: KPI tiles, cost & latency charts

My solution: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

Free course by @Al_Grigor & @DataTalksClub: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 3. Medium

> *Medium allows longer posts. Use a compelling hook and keep the tone professional but accessible.*

---

**You Can't Improve What You Don't Measure: Building LLM Monitoring from Scratch (LLM Zoomcamp Module 5)**

I just completed Module 5 of LLM Zoomcamp — Monitoring — and it answered a question every previous module left open: once your RAG app is running, how do you know if it's actually working? This module builds the observability layer that turns a prototype into something you can operate with confidence.

It starts with a simple observation: every LLM call produces a rich signal — tokens used, response time, cost, the actual answer — that most people just discard. Module 5 captures all of it in a `LLMCallRecord` dataclass and persists it to SQLite, so every conversation becomes a data point you can query, chart, and act on.

**What I Built and Learned:**

📌 **LLMCallRecord and RAGWithMetrics** — Extended `RAGBase` with a `RAGWithMetrics` subclass that wraps every LLM call with a timer and cost calculator. After each call, a `LLMCallRecord` is stored with model name, prompt, answer, token counts, response time, and cost. Cost per model is calculated from a simple formula — for `gpt-5.4-mini`: `(input_tokens × 0.15 + output_tokens × 0.60) / 1_000_000`. That one line makes every question financially accountable.

📌 **SQLite persistence layer** — Built four focused modules: `db_init.py` (schema creation), `db_save.py` (save conversations), `db_feedback.py` (save judge + user feedback), `db_query.py` (aggregate queries for the dashboard). Separating these concerns made each piece easy to test and extend independently.

📌 **Streamlit chat app with dual feedback** — The chat UI (`app.py`) goes beyond a basic Q&A box: after every answer, it automatically runs an LLM judge (`RelevanceVerdict` structured output — RELEVANT / PARTLY_RELEVANT / NON_RELEVANT) and also shows +1 / −1 buttons for the user. Both feedback signals are stored independently, which means you can later compare whether human ratings and LLM-judge ratings agree — or diverge in interesting ways.

📌 **Live monitoring dashboard** — `dashboard.py` uses Streamlit to show four KPI tiles (total conversations, avg response time, total cost, avg tokens), a cost-over-time line chart, a response-time-over-time line chart, and a scrollable list of recent conversations. All driven by live SQLite queries — refresh the page and it reflects the latest data.

📌 **Simulated data generator** — `generate_data.py` generates 100 fake conversations with randomised feedback in a single run (or streams them one per second in live mode). This lets you test and demo the dashboard without needing real users, and it produces realistic distributions for cost and latency that stress-test your aggregation queries.

**My homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

This is part of the free LLM Zoomcamp course by Alexey Grigorev and DataTalksClub. Highly recommended if you're building anything with LLMs: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 4. Reddit

> *Post to r/MachineLearning or r/learnmachinelearning. Reddit values genuine learning and discussion over self-promotion. Keep it conversational.*

---

**Finished Module 5 of LLM Zoomcamp — Monitoring. Here's how I built a cost + latency dashboard for a RAG app from scratch.**

Just wrapped up Module 5 of the free LLM Zoomcamp course. This one was about giving your LLM application the observability it needs to actually run in production — tracking cost, latency, and user feedback for every conversation.

**What actually clicked for me:**

**Every LLM call is a data point, not just a response.** Wrapping the `responses.create()` call with a timer and a cost formula gives you a `LLMCallRecord` for every question asked. Persisting that to SQLite means your entire conversation history becomes queryable. It sounds obvious in retrospect, but most tutorial code throws away all of this.

**Dual feedback catches different failure modes.** The app records both an automatic LLM-judge verdict (RELEVANT / PARTLY_RELEVANT / NON_RELEVANT) and a user +1 / −1 score for each answer. These two signals don't always agree — a judge can mark an answer as RELEVANT while the user rates it −1 because it was technically correct but unhelpful in tone. Having both lets you investigate those disagreements instead of being blind to them.

**Cost per call is not just a number — it's a ranking.** Once you have cost in your database, you can sort conversations by cost. Questions that hit expensive reasoning chains bubble up immediately. On my simulated data, the variance in cost across questions was surprisingly high, and you'd never know without tracking it.

**A data generator is essential for testing a dashboard.** Before you have real users, `generate_data.py` fills your database with 100 randomised conversations (or streams them live at 1/second). Testing aggregations and charts against realistic data distributions is qualitatively different from testing against 3 hand-crafted rows.

My solution for the homework: https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

Course is free and open: https://github.com/DataTalksClub/llm-zoomcamp/

Curious whether anyone here tracks LLM-judge vs. user feedback agreement rates in production — feels like that divergence metric could be really useful for catching prompt regressions.

---

## 5. Dev.to

> *Dev.to is developer-focused. Use tags, be technical, and write like you're sharing a project post.*

---

**I Built a Cost + Latency Monitoring Dashboard for a RAG App — LLM Zoomcamp Module 5**

*Tags: #llm #machinelearning #rag #python #streamlit #monitoring #llmops*

---

Just finished Module 5 of [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp/) — Monitoring. Here's a developer-focused breakdown of what I built to add production observability to a RAG application.

**The Problem: RAG Apps Are Black Boxes by Default**

After Modules 1–4, I had a working RAG app with keyword search, vector search, hybrid search, and evaluation metrics. But once it's running, how do you know if it's healthy? Are costs trending up? Are slow responses clustered around specific questions? Is the LLM judge agreeing with users? This module answers all of that.

**LLMCallRecord and RAGWithMetrics**

```python
@dataclass
class LLMCallRecord:
    model: str
    prompt: str
    answer: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response_time: float
    cost: float
    timestamp: datetime = field(default_factory=datetime.now)

    @staticmethod
    def calculate_cost(model, usage):
        if "gpt-5.4-mini" in model:
            return (usage.input_tokens * 0.15 + usage.output_tokens * 0.60) / 1_000_000
        return 0
```

`RAGWithMetrics` wraps `_call_llm()` with `time.time()` before and after, then builds a `LLMCallRecord` from the response's usage object and saves it to `self.last_call` for the app layer to persist.

**SQLite Persistence**

Four modules, each with one responsibility:

```
db_init.py     → CREATE TABLE IF NOT EXISTS conversations, feedback
db_save.py     → save_conversation(record, question, course) → conversation_id
db_feedback.py → save_feedback(conversation_id, source, relevance=None, score=None)
db_query.py    → get_conversations(), get_stats(), get_relevance_stats(), get_user_feedback_stats()
```

`get_stats()` returns a single dataclass with `total`, `avg_response_time`, `total_cost`, `avg_tokens` — exactly what the dashboard KPI tiles need.

**Streamlit App with Dual Feedback**

```python
# After every answer, auto-run the judge:
relevance, explanation = evaluate_relevance(user_input, answer)
save_feedback(conversation_id, "judge", relevance=relevance, explanation=explanation)

# Also show user buttons:
if st.button("+1"):
    save_feedback(cid, "user", score=1)
if st.button("-1"):
    save_feedback(cid, "user", score=-1)
```

`RelevanceVerdict` is a Pydantic model with `relevance: Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]` and an `explanation` field — the explanation is what makes a non-relevant verdict actionable rather than just a label.

**Monitoring Dashboard**

```python
stats = get_stats()
col1.metric("Total conversations", stats.total)
col2.metric("Avg response time", f"{stats.avg_response_time:.2f}s")
col3.metric("Total cost", f"${stats.total_cost:.4f}")
col4.metric("Avg tokens", f"{stats.avg_tokens:.0f}")

st.line_chart(df, x="timestamp", y="cost")
st.line_chart(df, x="timestamp", y="response_time")
```

Four KPI tiles + two time-series charts + recent conversations list, all from live SQLite queries. Refresh to update.

**Data Generator for Testing**

```python
def generate_live():
    while True:
        generate_one()   # random question + answer + judge feedback + user score
        time.sleep(1)
```

Streaming 1 record/second lets you watch the dashboard update in real time without needing real users — essential for demo and integration testing.

**My homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

**Course link (free):** https://github.com/DataTalksClub/llm-zoomcamp/

---

## 6. Quora

> *Quora works best as an answer to a question, or a story post. Educational and informative tone.*

---

**How do you monitor an LLM application in production? Here's what I built in LLM Zoomcamp Module 5.**

I just finished Module 5 of LLM Zoomcamp, which focused on building a proper monitoring layer for a RAG application — and I want to share the most important things I took away.

**Why monitoring an LLM app is different from monitoring a traditional API**

A traditional API either returns the right value or it doesn't. An LLM API always returns *something* — but that something might be irrelevant, hallucinated, or correct but expensive. You need to track three things simultaneously: is the answer good (quality), how long did it take (latency), and how much did it cost (cost). None of these can be inferred from the others.

**What I Built in Module 5**

The module has four main components:

**1. Metrics capture per call.** Every call to `responses.create()` is wrapped with a timer and a cost formula. The result is a `LLMCallRecord` dataclass — model, prompt, answer, input tokens, output tokens, response time, cost, timestamp. That one record contains everything you need for observability.

**2. Persistent storage.** Conversations and feedback are saved to SQLite via focused modules (`db_save.py`, `db_feedback.py`). This is the difference between observability you can query tomorrow and observability that only exists in your terminal scrollback.

**3. Dual feedback: judge + user.** The chat app runs an automatic LLM-judge (`RelevanceVerdict` — RELEVANT / PARTLY_RELEVANT / NON_RELEVANT) after every answer, and also captures user +1/−1 thumbs ratings. These two signals often disagree, and that disagreement is itself informative — it flags cases where the answer was technically relevant but not useful in context.

**4. Live dashboard.** A Streamlit dashboard shows four KPI tiles (total conversations, avg response time, total cost, avg tokens) and two time-series line charts (cost over time, response time over time). All from live SQLite queries — no external observability platform needed for a self-hosted prototype.

**The Key Insight: Aggregate Metrics Reveal What Individual Queries Hide**

A single slow response might be a fluke. A cost spike on a specific class of questions is a bug. A sustained upward trend in `avg_response_time` is a capacity issue. You only see any of these if you're collecting and charting the data — and this module builds exactly that infrastructure from scratch.

**My homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

The course is completely free: https://github.com/DataTalksClub/llm-zoomcamp/

---

## 7. Hashnode

> *Hashnode is a developer blogging platform. Use tags, write like a technical blog post with a punchy intro.*

---

**Monitoring LLM Apps: Cost, Latency, and User Feedback From Scratch — LLM Zoomcamp Module 5**

*Tags: llm, monitoring, llmops, rag, streamlit, python, machinelearning*

---

Module 5 of LLM Zoomcamp just wrapped up, and it's the module that turns a RAG prototype into something you can actually operate. The topic: Monitoring — capturing cost, latency, and feedback for every LLM call, persisting it to SQLite, and surfacing it in a live dashboard built with Streamlit.

Here's what I learned and built.

---

### The Core Insight: A Response Is Also a Data Point

Every call to `responses.create()` returns not just an answer but a full usage object: input tokens, output tokens, model name. Wrap that call with a timer and a cost formula, and you've turned a black-box response into a structured, queryable record. Module 5 makes this concrete with `LLMCallRecord` and `RAGWithMetrics`.

---

### What I Built

**✦ LLMCallRecord + RAGWithMetrics**

```python
class RAGWithMetrics(RAGBase):
    def llm(self, prompt):
        start_time = time.time()
        response = self._call_llm(prompt)
        response_time = time.time() - start_time
        self._log_response(prompt, response, response_time)
        return response.output_text
```

`_log_response` builds a `LLMCallRecord` from the response's usage object and stores it in `self.last_call`. The app layer reads `assistant.last_call` after each query and persists it to the database.

**✦ SQLite Persistence (4-module layout)**

| Module | Responsibility |
|---|---|
| `db_init.py` | Schema creation — conversations + feedback tables |
| `db_save.py` | `save_conversation(record, question, course)` → `conversation_id` |
| `db_feedback.py` | `save_feedback(id, source, relevance=None, score=None)` |
| `db_query.py` | Aggregation queries for dashboard KPIs and charts |

**✦ Streamlit Chat App with Dual Feedback**

```python
# Auto judge runs after every answer
relevance, explanation = evaluate_relevance(user_input, answer)
save_feedback(conversation_id, "judge", relevance=relevance, explanation=explanation)

# User can also rate
if st.button("+1"):
    save_feedback(cid, "user", score=1)
if st.button("-1"):
    save_feedback(cid, "user", score=-1)
```

`RelevanceVerdict` uses `Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]` with a mandatory `explanation` field. The explanation is what makes a low-quality verdict actionable: you can read it and understand *why* the judge disagreed.

**✦ Monitoring Dashboard**

```python
stats = get_stats()
col1.metric("Total conversations", stats.total)
col2.metric("Avg response time", f"{stats.avg_response_time:.2f}s")
col3.metric("Total cost", f"${stats.total_cost:.4f}")
col4.metric("Avg tokens", f"{stats.avg_tokens:.0f}")

st.line_chart(df, x="timestamp", y="cost")
st.line_chart(df, x="timestamp", y="response_time")
```

**✦ Data Generator**

`generate_data.py` creates 100 conversations in a batch or streams them live at 1/second for real-time dashboard testing. 70% of simulated conversations get a judge relevance score; 50% get a user +1/−1 rating — matching realistic feedback engagement rates.

---

### Key Takeaways for Production

| Concern | Approach |
|---|---|
| Tracking cost | Calculate from usage object per call, not estimated in advance |
| Tracking latency | Wall-clock timer around `responses.create()` only |
| Quality signal | LLM-judge (structured output) + user feedback independently |
| Judge vs user disagreement | Store both — the divergence is itself a signal |
| Dashboard without real users | Data generator simulating realistic traffic distributions |
| Avoiding external dependencies | SQLite + Streamlit — zero infra for a self-hosted prototype |

---

**Homework solution:** https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/05-monitoring/code.ipynb

**Free course:** https://github.com/DataTalksClub/llm-zoomcamp/

Built during [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp/) by DataTalksClub & Alexey Grigorev.
