# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

`huggingface-hub` and `jupyter` are dev-only dependencies — install them with:

```bash
uv sync --all-groups
```

Download model weights before running anything else (saved to `models/Xenova/all-MiniLM-L6-v2/`):

```bash
python download.py
```

Run the homework notebook:

```bash
jupyter notebook homework-2.ipynb
```

## Architecture

```
download.py      → pulls tokenizer.json + model.onnx from Hugging Face Hub
                   tries onnx/model.onnx → onnx/encoder_model.onnx → model.onnx
                   also fetches model.onnx_data if present (external data format)

embedder.py      → Embedder(path)
                     encode(text)          → float32 ndarray (384,), L2-normalised
                     encode_batch(texts)   → float32 ndarray (N, 384), mean-pooled + normalised
                   tokenizer.enable_padding() is called per batch; only feeds input names
                   the ONNX session actually declares (handles models without token_type_ids)

homework-2.ipynb → five-question pipeline:
                   Q1  embed a query string, read v[0]
                   Q2  cosine similarity between query and a specific page vector
                   Q3  chunk all pages (size=2000, step=1000), embed in batches of 50,
                       find best chunk by argmax dot product
                   Q4  VectorSearch (minsearch) — fit on chunk matrix X, search by vector
                   Q5  compare VectorSearch vs minsearch.Index (text search) top-5 results
```

## Key design points

- `gitsource.GithubRepositoryDataReader` fetches markdown pages from a pinned commit; `chunk_documents(size, step)` produces overlapping chunks.
- Because vectors are L2-normalised, dot product equals cosine similarity — no extra computation needed.
- `minsearch.VectorSearch` takes the pre-computed embedding matrix and document list; `minsearch.Index` does BM25-style text search over the same chunks.
- The `models/` directory is gitignored — always run `download.py` in a fresh clone.
