"""Command-line entry point for querying the course FAQ assistant."""

from __future__ import annotations

import argparse

from openai import OpenAI

from ingest import build_index, load_faq_data
from rag_helper import RAGBase


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the FAQ assistant."""
    parser = argparse.ArgumentParser(
        description="Ask a question about the LLM Zoomcamp FAQ."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="I just discovered the course. Can I join now?",
        help="The question to ask the FAQ assistant.",
    )
    return parser.parse_args()


def main() -> None:
    """Load the FAQ corpus, build the index, and answer a question."""
    args = parse_args()

    documents = load_faq_data()
    index = build_index(documents)
    client = OpenAI()
    assistant = RAGBase(index=index, llm_client=client)

    answer = assistant.rag(args.query)
    print(answer)


if __name__ == "__main__":
    main()
