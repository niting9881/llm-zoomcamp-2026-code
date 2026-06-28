# Lesson Learned: Lightweight Embeddings with ONNX Runtime

> Source: [09-onnx-embedder.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/02-vector-search/lessons/09-onnx-embedder.md)

---

## What is ONNX?

**ONNX** (Open Neural Network Exchange) is an open format for representing machine learning models. Think of it as a universal file format — like PDF for documents, but for neural networks. A model trained in PyTorch, TensorFlow, or JAX can be exported to ONNX format and then run anywhere using the **ONNX Runtime**, a lightweight execution engine.

For embedding tasks (turning text into vectors), ONNX Runtime loads the same model weights and produces **identical results** to sentence-transformers — without needing PyTorch installed at all.

---

## ONNX vs PyTorch (sentence-transformers)

| | sentence-transformers | ONNX Runtime |
|---|---|---|
| **Underlying engine** | PyTorch | ONNX Runtime |
| **Install size** | ~4.8 GB, 58 packages | ~147 MB, 27 packages |
| **GPU libraries** | Pulls in CUDA/Nvidia libs | Not required |
| **Output vectors** | Identical | Identical |
| **Best for** | Development, experiments | Production, deployment |
| **Runs on** | Needs Python + PyTorch stack | Anywhere (Docker, serverless, edge) |

**Key insight:** `sentence-transformers` is convenient but heavy. ONNX Runtime gives you the same embeddings at **33× smaller** footprint.

---

## Why Use ONNX? — The Benefits

1. **Tiny install** — 147 MB vs 4.8 GB means faster Docker builds, cheaper serverless cold starts, and lower storage costs.
2. **No CUDA required** — runs on CPU without Nvidia drivers. Works in any Codespace or basic cloud VM.
3. **Framework-agnostic** — the same `.onnx` file works regardless of whether the model was originally trained in PyTorch or TensorFlow.
4. **Pre-converted models available** — the Xenova organisation on Hugging Face publishes ready-to-use ONNX versions of the most popular sentence embedding models.
5. **Same API** — you call `embed.encode(text)` exactly as before; nothing in the search pipeline changes.
6. **Deploy anywhere** — small Docker images, serverless functions (AWS Lambda, Cloud Run), and even edge devices.

---

## Visual Workflow

```
                     ┌─────────────────────────────────────────────────┐
                     │            ONNX Embedding Pipeline               │
                     └─────────────────────────────────────────────────┘

  Raw text
     │
     ▼
┌─────────────┐
│  Tokenizer  │  tokenizer.json   →  converts words → integer IDs + attention mask
└─────────────┘
     │
     │  input_ids, attention_mask
     ▼
┌─────────────┐
│  ONNX Model │  model.onnx       →  runs the transformer graph on CPU
│  (Runtime)  │
└─────────────┘
     │
     │  hidden states  (tokens × 384 dimensions)
     ▼
┌─────────────┐
│ Mean Pooling│  weighted average over tokens using attention mask
└─────────────┘
     │
     │  single vector  (384 dimensions)
     ▼
┌─────────────┐
│  L2 Normalize│  divide by vector magnitude → unit vector
└─────────────┘
     │
     ▼
  Float32 vector  [−1 … +1] × 384
  (ready for dot-product similarity search)


  Query vector  ──┐
                  ├──► dot product ──► similarity score ──► ranked results
  Doc vectors   ──┘
```

---

## Setup

```bash
# Create a new project
mkdir my-onnx-project && cd my-onnx-project
uv init --no-workspace

# Core runtime dependencies (production)
uv add onnxruntime tokenizers numpy tqdm minsearch

# Dev-only: needed once to download the model
uv add --dev huggingface-hub jupyter
```

Download the model once (saved to `models/`):

```bash
python download.py        # fetches tokenizer.json + model.onnx from Hugging Face
```

Add models to `.gitignore` — they are large binary files, not source code:

```
models/
```

---

## The Embedder Class — How It Works

`embedder.py` wraps the four-step pipeline in a simple `encode` interface:

```python
class Embedder:
    def __init__(self, path="models/Xenova/all-MiniLM-L6-v2"):
        # loads tokenizer.json and model.onnx from the given path
        ...

    def encode(self, text) -> np.ndarray:
        # returns a single normalised float32 vector of shape (384,)
        ...

    def encode_batch(self, texts) -> np.ndarray:
        # returns shape (N, 384) — efficient for large datasets
        ...
```

---

## Sample Example: Comparing Text Similarity

```python
from embedder import Embedder

embed = Embedder()   # loads model once

q1 = "Can I still join the course after the start date?"
q2 = "How to install Docker on Windows?"
doc = "You don't need to register. You can start learning and submit homework anytime."

v1  = embed.encode(q1)
v2  = embed.encode(q2)
dv  = embed.encode(doc)

print(v1.dot(dv))   # higher — q1 is about registration, same topic as doc
print(v2.dot(dv))   # lower  — q2 is about Docker, unrelated to the doc
```

**Why dot product?** Because both vectors are L2-normalised, `a.dot(b)` equals cosine similarity. Values range from −1 (opposite) to +1 (identical). No extra math needed.

---

## Sample Example: Batch Embedding + Search

```python
import numpy as np
from tqdm.auto import tqdm
from embedder import Embedder

embed = Embedder()
documents = [...]   # list of dicts with "question" and "answer" keys

# Combine question + answer into one string per document
texts = [doc["question"] + " " + doc["answer"] for doc in documents]

# Embed in batches of 50 (efficient memory use)
batch_size = 50
X = []

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i + batch_size]
    X.extend(embed.encode_batch(batch))

X = np.array(X)   # shape: (num_docs, 384)

# Search
query = "Can I still join the course after the start date?"
v_query = embed.encode(query)

scores  = X.dot(v_query)          # dot product against every doc vector
best_idx = np.argmax(scores)      # index of the most similar document

print(documents[best_idx])
```

---

## Available Models (Plug-and-Play)

All models below work with the same `Embedder` class — just change the model name in `download.py` and the path in `Embedder()`:

| Model | Dimensions | Notes |
|---|---|---|
| `Xenova/all-MiniLM-L6-v2` | 384 | Best small general-purpose model |
| `Xenova/all-MiniLM-L12-v2` | 384 | Better quality, slightly slower |
| `Xenova/bge-small-en-v1.5` | 384 | Strong retrieval, English |
| `Xenova/bge-base-en-v1.5` | 768 | Stronger retrieval, English |
| `Xenova/gte-small` | 384 | Lightweight modern model |
| `Xenova/multilingual-e5-small` | 384 | Multilingual retrieval |
| `Xenova/paraphrase-multilingual-MiniLM-L12-v2` | 384 | Multilingual paraphrase |

```python
# Switch model by changing one line
embed = Embedder("models/Xenova/bge-base-en-v1.5")
v = embed.encode("your text here")
print(v.shape)   # (768,)
```

---

## When to Use What

```
Are you experimenting or prototyping?
    YES  →  use sentence-transformers (simpler install, familiar API)
    NO   ↓
Are you deploying to production / CI / serverless / Docker?
    YES  →  use ONNX Runtime  (33x smaller, no CUDA, same results)
```

---

## Key Takeaways

- ONNX is a **model format**, not a training framework. You export a trained model to `.onnx` once, then run it anywhere.
- ONNX Runtime replaces the entire PyTorch stack for **inference only** — you cannot train with it.
- The `Embedder` class hides the four steps (tokenize → run → pool → normalise) behind a single `encode()` call.
- Vector output is **identical** to sentence-transformers — your search pipeline does not need to change.
- For production workloads, the 33× size reduction directly translates to lower costs and faster deployments.
