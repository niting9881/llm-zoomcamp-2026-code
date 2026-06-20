"""Retrieval-augmented generation helpers for the course FAQ assistant."""

from __future__ import annotations

from typing import Any

INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()

DEFAULT_MODEL = "gpt-5.4-mini"


class RAGBase:
    """Run search, prompt construction, and answer generation for a FAQ bot."""

    def __init__(
        self,
        index: Any,
        llm_client: Any,
        instructions: str = INSTRUCTIONS,
        prompt_template: str = PROMPT_TEMPLATE,
        course: str = "llm-zoomcamp",
        model: str = DEFAULT_MODEL,
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query: str, num_results: int = 5) -> list[dict[str, Any]]:
        """Search the indexed FAQ corpus for the most relevant documents."""
        boost_dict = {"question": 3.0, "section": 0.5}
        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict,
        )

    def build_context(self, search_results: list[dict[str, Any]]) -> str:
        """Format retrieved documents into a readable context block."""
        lines: list[str] = []

        for doc in search_results:
            lines.extend(
                [
                    str(doc.get("section", "")),
                    f"Q: {doc.get('question', '')}",
                    f"A: {doc.get('answer', '')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    def build_prompt(self, query: str, search_results: list[dict[str, Any]]) -> str:
        """Build the final prompt passed to the language model."""
        context = self.build_context(search_results)
        return self.prompt_template.format(question=query, context=context)

    def _build_input_messages(self, prompt: str) -> list[dict[str, str]]:
        """Create the message payload used for the model request."""
        return [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt},
        ]

    def llm(self, prompt: str) -> str:
        """Generate a response from the configured LLM client."""
        response = self.llm_client.responses.create(
            model=self.model,
            input=self._build_input_messages(prompt),
        )
        return response.output_text

    def rag(self, query: str) -> str:
        """Run the complete retrieval-augmented generation flow."""
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        return self.llm(prompt)
        