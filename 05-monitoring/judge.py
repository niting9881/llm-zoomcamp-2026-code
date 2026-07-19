import json

from pydantic import BaseModel
from typing import ClassVar, Literal
from openai import OpenAI
from dotenv import load_dotenv

from evaluation_utils import llm_structured_retry

class RelevanceVerdict(BaseModel):
    relevance: Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]
    explanation: str

    judge_instructions: ClassVar[str] = """
    You are an expert evaluator for a RAG system.
    Analyze the relevance of the generated answer to the given question.

    Classify the answer as:
    - RELEVANT: the answer addresses the question
    - PARTLY_RELEVANT: the answer partially addresses the question
    - NON_RELEVANT: the answer does not address the question
    """.strip()

    judge_prompt: ClassVar[str] = """
    Question: {question}
    Generated Answer: {answer}
    """.strip()
    @staticmethod
    def evaluate_relevance(question, answer, client=None):
        if client is None:
            client = OpenAI()

        prompt = RelevanceVerdict.judge_prompt.format(
            question=question,
            answer=answer
        )

        result, usage = llm_structured_retry(
            client,
            RelevanceVerdict.judge_instructions,
            prompt,
            RelevanceVerdict,
        )

        return result.relevance, result.explanation

def main():
    load_dotenv()

    question = "Can I still join the course?"
    answer = "Yes, you can still join. The course is self-paced."

    relevance, explanation = RelevanceVerdict.evaluate_relevance(question, answer)
    print(relevance)
    print(explanation)

if __name__ == "__main__":
    main()