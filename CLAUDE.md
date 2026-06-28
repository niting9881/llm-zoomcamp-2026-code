# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

This repo has two independent Python projects, each with its own virtualenv managed by `uv`:

| Directory | Purpose |
|---|---|
| `/` (root) | Keyword-search RAG pipeline using MinSearch + OpenAI API |
| `llm-zoomcamp-hw2/` | Local-embedding RAG variant using ONNX + `onnxruntime` (no GPU/API required) |

## Environment setup

Both projects use `uv` and Python 3.12. Always activate or target the correct venv for the sub-project you're working in.

```bash
# Root project
uv sync

# HW2 sub-project
cd llm-zoomcamp-hw2 && uv sync
```

The root project requires `OPENAI_API_KEY` in `.env` (already gitignored). The HW2 sub-project runs entirely locally via ONNX.

## Running the root RAG assistant

```bash
# Ask a question (fetches FAQ data live, builds index, calls OpenAI)
python main.py "Can I still join the course after it started?"

# Rebuild and inspect the index without asking a question
python -c "from ingest import load_faq_data, build_index; docs = load_faq_data(); idx = build_index(docs); print(len(docs), 'docs')"
```

## Running the HW2 ONNX embedder

```bash
cd llm-zoomcamp-hw2

# Download the ONNX model weights first (saves to models/Xenova/all-MiniLM-L6-v2/)
python download.py

# Run the homework notebook
jupyter notebook homework-2.ipynb
```

## Architecture: root project

```
ingest.py          → load_faq_data()  fetches JSON from datatalks.club FAQ pages
                   → build_index()    wraps MinSearch Index (text + keyword fields)

rag_helper.py      → RAGBase          orchestrates: search → build_prompt → llm → RAGResult
                     RAGResult        dataclass: answer str, input_tokens int, search_results list

main.py            → CLI entry point; wires OpenAI() client into RAGBase
```

- Search boosts `question` field (3×) over `section` (0.5×) and filters by `course`.
- The LLM client uses `client.responses.create(...)` — this is the OpenAI Responses API, not `chat.completions`.
- `RAGBase` accepts any index object that has a `.search()` method, making it easy to swap backends.

## Architecture: llm-zoomcamp-hw2

```
download.py   → downloads tokenizer.json + model.onnx from HuggingFace Hub
                (tries onnx/model.onnx, onnx/encoder_model.onnx, model.onnx in that order)
                saves to models/<repo-id>/

embedder.py   → Embedder class
                  __init__: loads tokenizer + onnxruntime session from models/ path
                  encode(text)          → single normalized float32 vector
                  encode_batch(texts)   → stacked array, mean-pooled over attention mask
```

The embedder is CPU-only (`CPUExecutionProvider`). Normalisation is on by default (L2 norm per row).

## SQLite databases (root)

- `faq.db` — keyword-search index (gitignored)
- `faq_vectors2.db` — vector-search index (not yet gitignored; large binary)

## Key dependencies

| Package | Role |
|---|---|
| `minsearch` | Lightweight BM25-style in-memory search |
| `openai` | OpenAI Responses API client |
| `sentence-transformers` | HuggingFace embedding models (root project) |
| `sqlitesearch` | SQLite-backed search index |
| `onnxruntime` + `tokenizers` | Local ONNX inference in hw2 |
| `gitsource` | Fetch data from git repos |
| `toyaikit` | Lightweight AI toolkit utilities |
