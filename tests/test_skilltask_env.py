"""Tests for the fork-local generic ``skilltask`` env (no network)."""
from __future__ import annotations

import json

import pytest

from skillopt.envs.skilltask import rollout as rollout_mod
from skillopt.envs.skilltask.adapter import SkillTaskAdapter
from skillopt.envs.skilltask.dataloader import normalize_item


def test_normalize_item_requires_expected_or_rubric():
    with pytest.raises(ValueError, match="expected' or 'rubric"):
        normalize_item({"id": "a", "input": "hi"})
    item = normalize_item({"id": 1, "prompt": "q", "rubric": ["cites path", "no filler"]})
    assert item["id"] == "1"
    assert item["rubric"] == "- cites path\n- no filler"


def test_grade_string_modes():
    item = {"question": "q", "ground_truth": "Paris", "rubric": "", "grader": ""}
    kw = {"pass_threshold": 0.7, "judge_max_tokens": 64}
    assert rollout_mod.grade(item, " paris ", default_grader="exact", **kw)[:2] == (1, 1.0)
    assert rollout_mod.grade(item, "It is Paris.", default_grader="auto", **kw)[:2] == (1, 1.0)
    assert rollout_mod.grade(item, "Lyon", default_grader="contains", **kw)[:2] == (0, 0.0)


def test_grade_judge_parses_and_clamps(monkeypatch):
    monkeypatch.setattr(rollout_mod, "chat_optimizer",
                        lambda **kw: ('noise {"score": 1.7, "reason": "great"}', {}))
    item = {"question": "q", "ground_truth": "", "rubric": "be brief", "grader": ""}
    hard, soft, reason = rollout_mod.grade(item, "ok", default_grader="auto",
                                           pass_threshold=0.7, judge_max_tokens=64)
    assert (hard, soft, reason) == (1, 1.0, "great")
    monkeypatch.setattr(rollout_mod, "chat_optimizer", lambda **kw: ("no json", {}))
    assert rollout_mod.grade(item, "ok", default_grader="judge",
                             pass_threshold=0.7, judge_max_tokens=64)[:2] == (0, 0.0)


def test_run_batch_writes_conversations(tmp_path, monkeypatch):
    monkeypatch.setattr(rollout_mod, "chat_target", lambda **kw: ("Paris", {}))
    items = [normalize_item({"id": "t1", "input": "Capital of France?", "expected": "Paris"}),
             normalize_item({"id": "t2", "input": "Capital of Spain?", "expected": "Madrid"})]
    results = rollout_mod.run_batch(items=items, skill_content="# skill", out_root=str(tmp_path))
    assert [r["hard"] for r in results] == [1, 0]
    assert "fail_reason" in results[1]
    convo = json.loads((tmp_path / "predictions" / "t1" / "conversation.json").read_text())
    assert convo[0] == {"role": "system", "content": "# skill"}


def test_adapter_ratio_split(tmp_path):
    data = tmp_path / "tasks.jsonl"
    data.write_text("\n".join(json.dumps({"id": f"t{i}", "input": f"q{i}", "expected": "x"})
                              for i in range(10)), encoding="utf-8")
    adapter = SkillTaskAdapter(data_path=str(data), split_output_dir=str(tmp_path / "split"))
    adapter.setup({"env": "skilltask", "out_root": str(tmp_path)})
    loader = adapter.get_dataloader()
    assert (len(loader.train_items), len(loader.val_items), len(loader.test_items)) == (5, 3, 2)
    assert adapter.get_task_types() == ["skilltask"]
    with pytest.raises(ValueError, match="grader"):
        SkillTaskAdapter(grader="bogus")
