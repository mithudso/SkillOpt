"""Data loader for the ``skilltask`` env.

Accepted item fields (JSON array or JSONL):

- ``id`` (required, unique string)
- ``input`` / ``prompt`` / ``question`` — the user message sent to the target
- ``expected`` / ``answer`` — optional reference answer
- ``rubric`` — optional grading criteria for the LLM judge
- ``grader`` — optional per-item override: ``exact`` | ``contains`` | ``judge``
- ``task_type`` / ``category`` — optional grouping label
"""
from __future__ import annotations

from skillopt.datasets.base import SplitDataLoader


def normalize_item(raw: dict) -> dict:
    item_id = str(raw.get("id") or raw.get("uid") or "").strip()
    if not item_id:
        raise ValueError(f"skilltask item is missing 'id': {raw!r}")
    prompt = str(raw.get("input") or raw.get("prompt") or raw.get("question") or "").strip()
    if not prompt:
        raise ValueError(f"skilltask item {item_id!r} has no input/prompt/question")
    expected = str(raw.get("expected") or raw.get("answer") or "").strip()
    rubric = raw.get("rubric") or ""
    if isinstance(rubric, list):
        rubric = "\n".join(f"- {line}" for line in rubric)
    rubric = str(rubric).strip()
    if not expected and not rubric:
        raise ValueError(f"skilltask item {item_id!r} needs 'expected' or 'rubric'")
    return {
        "id": item_id,
        "question": prompt,
        "ground_truth": expected,
        "rubric": rubric,
        "grader": str(raw.get("grader") or "").strip().lower(),
        "task_type": str(raw.get("task_type") or raw.get("category") or "skilltask"),
    }


class SkillTaskDataLoader(SplitDataLoader):
    """Normalizes items after the base class reads each split's JSON file."""

    def load_split_items(self, split_path: str) -> list[dict]:
        return [normalize_item(row) for row in super().load_split_items(split_path)]
