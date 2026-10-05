"""Rollout and grading for the ``skilltask`` env."""
from __future__ import annotations

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from skillopt.model import chat_optimizer, chat_target

JUDGE_SYSTEM = (
    "You are a strict grader. Score how well RESPONSE satisfies the TASK under "
    "the RUBRIC (and matches EXPECTED when given). Reply with JSON only: "
    '{"score": <number 0..1>, "reason": "<one sentence>"}'
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _parse_judge(raw: str) -> tuple[float, str]:
    match = re.search(r"\{.*\}", raw or "", re.DOTALL)
    if not match:
        return 0.0, f"judge returned no JSON: {(raw or '')[:200]!r}"
    try:
        payload = json.loads(match.group(0))
        score = float(payload.get("score", 0.0))
    except (ValueError, TypeError, AttributeError):
        return 0.0, f"judge returned invalid JSON: {match.group(0)[:200]!r}"
    return min(max(score, 0.0), 1.0), str(payload.get("reason", ""))


def grade(item: dict, prediction: str, *, default_grader: str, pass_threshold: float,
          judge_max_tokens: int) -> tuple[int, float, str]:
    """Return ``(hard, soft, reason)`` for one prediction."""
    grader = item.get("grader") or default_grader
    expected = item.get("ground_truth", "")
    if grader == "auto":
        grader = "judge" if item.get("rubric") else "contains"
    if grader == "exact":
        ok = bool(expected) and _norm(prediction) == _norm(expected)
        return int(ok), float(ok), "exact match" if ok else "not an exact match"
    if grader == "contains":
        ok = bool(expected) and _norm(expected) in _norm(prediction)
        return int(ok), float(ok), "expected text found" if ok else "expected text missing"
    user = (
        f"TASK:\n{item['question']}\n\nRUBRIC:\n{item.get('rubric') or '(none)'}\n\n"
        f"EXPECTED:\n{expected or '(none)'}\n\nRESPONSE:\n{prediction}"
    )
    raw, _usage = chat_optimizer(system=JUDGE_SYSTEM, user=user,
                                 max_completion_tokens=judge_max_tokens, stage="judge")
    soft, reason = _parse_judge(raw)
    return int(soft >= pass_threshold), soft, reason


def _rollout_one(item: dict, skill_content: str, *, prediction_dir: Path, max_completion_tokens: int,
                 default_grader: str, pass_threshold: float, judge_max_tokens: int) -> dict:
    user = item["question"]
    try:
        prediction, _usage = chat_target(system=skill_content, user=user,
                                         max_completion_tokens=max_completion_tokens)
    except Exception as exc:  # keep the batch alive; a failed call scores 0
        prediction = ""
        hard, soft, reason = 0, 0.0, f"target call failed: {exc}"
    else:
        hard, soft, reason = grade(item, prediction, default_grader=default_grader,
                                   pass_threshold=pass_threshold, judge_max_tokens=judge_max_tokens)

    task_dir = prediction_dir / str(item["id"])
    task_dir.mkdir(parents=True, exist_ok=True)
    conversation = [
        {"role": "system", "content": skill_content},
        {"role": "user", "content": user},
        {"role": "assistant", "content": prediction},
    ]
    (task_dir / "conversation.json").write_text(
        json.dumps(conversation, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "id": str(item["id"]),
        "hard": hard,
        "soft": soft,
        "predicted_answer": prediction,
        "task_description": user,
        "question": user,
        "reference_text": "\n\n".join(
            part for part in (
                f"Expected: {item['ground_truth']}" if item.get("ground_truth") else "",
                f"Rubric:\n{item['rubric']}" if item.get("rubric") else "",
            ) if part),
        "task_type": item.get("task_type", "skilltask"),
        "target_system_prompt": skill_content,
        "target_user_prompt": user,
        "n_turns": 1,
    }
    if not hard:
        result["fail_reason"] = reason
    return result


def run_batch(*, items: list[dict], skill_content: str, out_root: str, workers: int = 4,
              max_completion_tokens: int = 4096, default_grader: str = "auto",
              pass_threshold: float = 0.7, judge_max_tokens: int = 1024) -> list[dict]:
    os.makedirs(out_root, exist_ok=True)
    prediction_dir = Path(out_root, "predictions")

    def _one(item: dict) -> dict:
        return _rollout_one(item, skill_content, prediction_dir=prediction_dir,
                            max_completion_tokens=max_completion_tokens, default_grader=default_grader,
                            pass_threshold=pass_threshold, judge_max_tokens=judge_max_tokens)

    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
        results = list(pool.map(_one, items))
    Path(out_root, "rollouts.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results
