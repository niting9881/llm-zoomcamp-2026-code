"""Utilities for fetching and indexing the course FAQ dataset."""

from __future__ import annotations

from typing import Any

import requests
from minsearch import Index

FAQ_INDEX_URL = "https://datatalks.club/faq/json/courses.json"
FAQ_BASE_URL = "https://datatalks.club/faq"
DEFAULT_TEXT_FIELDS = ("question", "section", "answer")
DEFAULT_KEYWORD_FIELDS = ("course",)


def _fetch_json(url: str) -> Any:
    """Fetch JSON data from a URL and raise on HTTP errors."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def load_faq_data(
    index_url: str = FAQ_INDEX_URL,
    base_url: str = FAQ_BASE_URL,
) -> list[dict[str, Any]]:
    """Download FAQ documents for all course pages.

    The course index is fetched first, then every course-specific FAQ page is
    requested and its entries are merged into a single list.
    """
    courses_raw = _fetch_json(index_url)
    if not isinstance(courses_raw, list):
        raise ValueError("The FAQ index must be a list of course entries.")

    documents: list[dict[str, Any]] = []

    for course in courses_raw:
        path = course.get("path")
        if not path:
            continue

        course_url = f"{base_url}{path}"
        course_data = _fetch_json(course_url)
        if isinstance(course_data, list):
            documents.extend(course_data)

    return documents


def build_index(
    documents: list[dict[str, Any]],
    text_fields: tuple[str, ...] = DEFAULT_TEXT_FIELDS,
    keyword_fields: tuple[str, ...] = DEFAULT_KEYWORD_FIELDS,
) -> Index:
    """Build a MinSearch index for FAQ documents.

    Parameters:
        documents: FAQ entries that include text and keyword fields.
        text_fields: Fields that should be tokenized for text search.
        keyword_fields: Fields used for exact matching.
    """
    index = Index(
        text_fields=list(text_fields),
        keyword_fields=list(keyword_fields),
    )
    index.fit(documents)
    return index