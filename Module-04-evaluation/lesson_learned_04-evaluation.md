# Lesson Learned: Evaluating Search, RAG, and Agents

> Source: [04-evaluation](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation)

---

## What is Evaluation?

In the earlier modules we built several ways to retrieve and answer questions: keyword search with minsearch, vector search, hybrid search with RRF, RAG pipelines, and agents with tool calling. What we never did was answer the obvious question — which one is actually *better*?

**Evaluation** is the discipline of replacing "this looks good" with a number you can compare across runs. Instead of eyeballing a handful of queries, you build a labeled test set, run every approach against it, and measure. Of everything in the LLM Zoomcamp course, this is the part that matters most — and the most tedious. It's also the only way to know your system still works after you change a prompt, swap a model, or tune a boost value.

There are two flavors:

- **Offline evaluation** — run the system against a fixed test dataset and compute metrics, *before* anything reaches a user. This is the module's focus.
- **Online evaluation** — collect real feedback, logs, and dashboards from production traffic *after* deployment (covered in Module 05).

---

## The Core Problem: Intuition Is Not Evidence

Before this module, boosting the `question` field 3x over `answer` and `section` in keyword search "sounded reasonable" — a query should match the FAQ question more than the answer text.

Measured against a real evaluation set, that intuition was wrong:

```text
boost=0.5:  hit_rate=0.911  mrr=0.801
boost=1.0:  hit_rate=0.924  mrr=0.814   ← best single-parameter result
boost=3.0:  hit_rate=0.899  mrr=0.769
boost=5.0:  hit_rate=0.871  mrr=0.740
boost=10.0: hit_rate=0.858  mrr=0.712
```

Increasing the question boost made results *worse*, not better. A full grid search later showed the opposite of the starting assumption: `answer` should be weighted roughly **2x** `question`, with almost no weight on `section`. Nobody would have found this by hand-checking a few queries — it only shows up once you measure across the whole dataset.

```
Without evaluation:
  Change a setting  →  "feels better"  →  ship it  →  hope

With evaluation:
  Change a setting  →  re-run evaluate()  →  compare metric  →  ship only if it moved
```

---

## Part 1: Ground Truth Generation (A → Q*)

You can't measure retrieval without knowing the *correct* answer for a set of questions. The trick used throughout this module is to generate that labeling with an LLM instead of a human:

```
   Original document (A)
          │
          ▼
   ┌─────────────────┐
   │  LLM, structured │   "Formulate 5 questions this
   │  output          │    student might ask that are
   │  (Questions      │    answered by this page"
   │   model)         │
   └─────────────────┘
          │
          ▼
   5 questions (Q*), each labeled with the source
   document's id / filename
```

Structured output (`responses.parse` + a Pydantic model) beats free-form text here because downstream code needs a reliable list, not a paragraph to parse:

```python
from pydantic import BaseModel

class Questions(BaseModel):
    questions: list[str]

result, usage = llm_structured(
    client, data_gen_instructions, user_prompt, Questions
)
```

Two details matter more than they first appear:

- **Ask for different wording than the source text.** If the generation prompt says "use as few words as possible from the record," the resulting questions look like real user queries instead of paraphrased FAQ text. Skip this and your metrics will look inflated — the search engine is matching vocabulary, not understanding.
- **Retry and parallelize once you scale past a handful of documents.** `llm_structured_retry` wraps the call with exponential backoff for transient API failures, and `ThreadPoolExecutor` + a `map_progress` helper turns "one call after another" into 5-6 calls in flight — the network wait, not the LLM, is the bottleneck.

In our homework run, generating 5 questions each for 3 lesson pages averaged **1353 input tokens per call** — a useful sanity check before firing off hundreds of calls at 72+ documents.

---

## Part 2: Search Evaluation — Hit Rate and MRR

Once you have ground truth, evaluating search is a three-step pipeline:

```
question ──▶ search_function(query) ──▶ top-N results
                                              │
                                    was the correct doc in there?
                                              │
                                              ▼
                                   relevance = [1,0,0,0,0]  (per query)
```

Turn each query's relevance list into two metrics:

| Metric | Answers | Formula |
|---|---|---|
| **Hit Rate** | Did the correct doc show up *anywhere* in the results? | `count(any 1 in line) / total queries` |
| **MRR** (Mean Reciprocal Rank) | Did it show up *near the top*? | `sum(1 / (rank+1) for first hit) / total queries` |

```python
def hit_rate(relevance):
    return sum(1 in line for line in relevance) / len(relevance)

def mrr(relevance):
    total = 0.0
    for line in relevance:
        for rank, hit in enumerate(line):
            if hit:
                total += 1 / (rank + 1)
                break
    return total / len(relevance)
```

Hit Rate is always the upper bound of MRR — a document buried at position 5 counts fully for Hit Rate but only scores `1/5` for MRR. **A high Hit Rate with a low MRR means the right document is *there*, just buried under noise the LLM has to sift through.**

The whole thing wraps into one reusable function:

```python
def evaluate(ground_truth, search_function):
    relevance_total = compute_relevance_total(ground_truth, search_function)
    return {"hit_rate": hit_rate(relevance_total), "mrr": mrr(relevance_total)}
```

From here on, comparing *any* retrieval approach is a one-line call: `evaluate(ground_truth, some_search_fn)`.

---

## Part 3: Comparing Keyword, Vector, and Hybrid Search

With `evaluate()` in hand, the module (and our homework) ran the same 360-question ground truth against three retrieval methods over the course-lesson chunks:

| Method | Hit Rate | MRR |
|---|---|---|
| Keyword (`text_search`, minsearch `Index`) | 0.758 | 0.594 |
| Vector (`vector_search`, minsearch `VectorSearch`) | 0.808 | 0.636 |
| Hybrid (RRF, `k=1`) | 0.858 | **0.672** |

The same single query can flip the intuition on its head: for the first ground-truth question ("What exactly is a retrieval-augmented generation system…"), **keyword search's top hit was the wrong page**, while **vector search nailed it on the first try** — even though, averaged across the whole dataset, keyword search isn't dramatically behind vector search. This is exactly why per-query anecdotes are unreliable and full-dataset measurement is not optional.

Hybrid search merges both ranked lists with **Reciprocal Rank Fusion (RRF)**, scoring every doc by its position (not its raw score, which lives on an incomparable scale) in each list:

```python
def rrf(result_lists, k=60, num_results=5):
    scores, docs = {}, {}
    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc
    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]
```

The constant `k` controls how sharply rank matters: a **smaller `k` rewards top positions more aggressively**, a **larger `k` flattens the gap** between rank 0 and rank 5. Sweeping `k` over `[1, 50, 100, 200]` on our data showed `k=1` gave the best MRR (0.672), with 50/100/200 converging to a nearly identical, slightly lower plateau (0.672 → 0.672 → 0.672, vs 0.858 hit-rate at k=1 dropping to 0.847 at higher k). The paper's default of `k=60` is a reasonable starting point, not a law — measure it on your own data.

---

## Part 4: Search Parameter Tuning

`evaluate()` turns every search knob — field boosts, top-K, filters, RRF's `k` — into something you sweep instead of guess:

```python
for boost in [0.5, 1.0, 3.0, 5.0, 10.0]:
    result = evaluate(ground_truth, lambda q, b=boost: search_boost(q, b))
    print(f"boost={boost}: {result}")
```

For a handful of parameters, brute-force grid search is cheap (about a second per combination on an in-memory index). Two practical limits worth knowing before you copy this pattern to a heavier pipeline:

- **When each evaluation takes minutes instead of seconds** (e.g. sweeping RAG or agent settings, which cost an LLM call per query), grid search becomes too expensive — reach for Bayesian optimization (e.g. `hyperopt`) instead, since it explores the space more efficiently by favoring likely-good combinations.
- **Top-K is a tradeoff, not a free lunch.** Returning more results improves Hit Rate (more chances to catch the right doc) but increases the context sent to the LLM, raising cost and making it harder for the model to find the signal in the noise.

---

## Part 5: RAG Evaluation — LLM as a Judge

Search evaluation only tells you retrieval works. It says nothing about whether the *final answer* is any good — and the generated answer will never match the original FAQ text word-for-word, since it's paraphrased by a generative model. Exact string matching is the wrong tool here.

The fix is the **A → Q* → A'** pattern:

```
A  (original FAQ answer)
     │
     ▼  LLM generates a question from A
Q*  (generated question)
     │
     ▼  RAG pipeline answers Q*
A'  (generated answer)
     │
     ▼  a second LLM call compares A and A'
"good" / "bad" + reasoning
```

The second LLM call is the **judge** — another structured-output call that decides whether `A'` is *semantically* equivalent to `A`, not textually identical:

```python
class AnswerEvaluation(BaseModel):
    reasoning: str
    score: Literal["good", "bad"]
```

Two things distinguish a useful judge from a rubber stamp:

- **Ask it to explain, not just score.** Requesting `reasoning` alongside `score` produces better classifications, and the reasoning is what you actually read when triaging failures — the score alone doesn't tell you *why* an answer failed (wrong doc retrieved? prompt dropped context? model ignored the context?).
- **The judge itself needs auditing.** It can be too lenient — marking an answer "good" even when the underlying retrieval was wrong. There is no shortcut here: you sample cases by hand, read the judge's reasoning, and decide whether you agree. You cannot use another judge to evaluate the judge. In the course's reference run this caught the failure mode directly: 379/395 answers scored "good," and the 16 "bad" ones were the most informative rows in the whole dataset — each pointed at a specific pipeline stage to go fix.

---

## Part 6: Agent Evaluation — Answer *and* Trajectory

Agents add a second axis beyond RAG: not just "was the final answer right" but "did the *path* it took to get there make sense." The judge needs to see both the answer and the tool-call trajectory:

```python
class AgentEvaluation(BaseModel):
    answer_reasoning: str
    answer_score: Literal["good", "bad"]
    trajectory_reasoning: str
    trajectory_score: Literal["good", "bad"]
```

The two scores diagnose different failures:

| answer_score | trajectory_score | Likely cause |
|---|---|---|
| good | good | Working as intended |
| bad | good | Retrieval was fine, but the model used the context poorly |
| bad | bad | Agent likely searched for the wrong thing, or stopped too early |
| good | bad | Got lucky — the trajectory should still be flagged for review |

A "good" trajectory isn't defined by call count — it's defined by relevance: the query includes the important keywords from the question, no duplicate searches with identical arguments, later searches (if any) refine rather than repeat, and the number of calls is proportionate to the question's difficulty (usually 1, occasionally 2-3, more than 3 needs a clear reason).

---

## When to Use What

| Scenario | Approach | Why |
|---|---|---|
| Comparing keyword vs. vector vs. hybrid retrieval | **Hit Rate + MRR** | Cheap, fast, no LLM call per evaluation — measures retrieval in isolation from generation |
| Tuning field boosts, top-K, or RRF's `k` | **Grid search + `evaluate()`** | A few seconds per combination on an in-memory index; turns guessing into measurement |
| Judging whether a RAG answer is *correct* | **LLM-as-a-judge (A→Q*→A')** | Exact-match scoring fails because generated text is never word-for-word identical to the source |
| Judging an agent's tool use, not just its answer | **Dual-score judge (answer + trajectory)** | A right answer can hide a bad search; a good trajectory can still produce a wrong answer |
| No production traffic yet | **Synthetic ground truth (LLM-generated Q*)** | Gives you a baseline before you have any real user queries to learn from |
| System is live | **Online evaluation** (feedback, logs, dashboards) | Synthetic data eventually diverges from what real users actually ask |

```
Do you have real user queries yet?
    NO   →  Generate synthetic ground truth (A → Q*), start with offline eval
    YES  ↓

Are you evaluating retrieval only, or the full answer?
    RETRIEVAL ONLY  →  Hit Rate / MRR — no LLM call needed per evaluation
    FULL ANSWER     →  LLM-as-a-judge (A → Q* → A')

Does the system use tools/agents?
    YES  →  Judge the answer AND the tool-call trajectory separately
    NO   →  Judge the answer only
```

---

## Key Takeaways

1. **Evaluation replaces intuition with evidence.** A boost value that "sounds right" can measurably hurt retrieval. The only way to know is to run the same ground truth through both settings and compare the number.

2. **One query proves nothing; the whole dataset does.** The same question can have keyword search miss and vector search hit — or vice versa. Anecdotal spot checks will point you in the wrong direction as often as the right one.

3. **Hit Rate and MRR answer different questions.** Hit Rate says "is the right document anywhere in the results." MRR says "is it near the top." A system can have great Hit Rate and mediocre MRR — that's a ranking problem, not a retrieval problem.

4. **RRF's `k` is a knob, not a constant.** The paper's default of 60 is a reasonable starting point; the value that actually maximizes MRR depends on your data and is worth sweeping.

5. **Synthetic ground truth needs a wording gap by design.** If generated questions echo the source document's phrasing, your metrics look inflated for the wrong reason. Explicitly instruct the generator to avoid copying the source text.

6. **LLM-as-a-judge only works when it explains itself.** Requesting `reasoning` alongside a `good`/`bad` score is what makes failed cases actionable instead of just a number to shrug at.

7. **You cannot outsource judging the judge.** A second LLM cannot validate the first judge's calls — someone has to read a sample of verdicts by hand and confirm they're trustworthy before relying on the score at scale.

8. **For agents, a right answer can hide a wrong process.** Scoring the final answer alone misses cases where the agent got lucky despite a bad trajectory (duplicate searches, irrelevant queries, stopping too early). Score the path, not just the destination.
