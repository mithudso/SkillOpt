"""Behavioral guards for metadata drift and protected-input exclusion."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import doc_inventory


def _git_paths(monkeypatch, names):
    monkeypatch.setattr(
        doc_inventory.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(stdout="\0".join(names).encode("utf-8") + b"\0"),
    )


def test_inventory_never_reads_protected_input_bodies(tmp_path, monkeypatch):
    names = ["data/private.json", "ckpt/checkpoint.md", "skillopt/prompts/system.md",
             "skillopt/envs/example/skills/initial.md", "skillopt_sleep/prompts/template.md", "module.py"]
    _git_paths(monkeypatch, names)
    (tmp_path / "module.py").write_text('"""Synthetic helper."""\n', encoding="utf-8")
    original = Path.read_text

    def guarded_read(path, *args, **kwargs):
        assert path == tmp_path / "module.py", f"protected input read: {path}"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read)
    cards, environment, calls, tools = doc_inventory.collect(tmp_path)
    assert [row["path"] for row in cards] == ["module.py"]
    assert not environment and not calls and not tools


def test_inventory_records_names_without_environment_values(tmp_path, monkeypatch):
    _git_paths(monkeypatch, ["module.py"])
    (tmp_path / "module.py").write_text(
        'import os\ndef example():\n    return os.getenv("SYNTHETIC_API_KEY", "never-export-this-value")\n',
        encoding="utf-8",
    )
    output = doc_inventory.render(tmp_path)
    environment = output["docs/environment-variables.md"]
    assert "SYNTHETIC_API_KEY" in environment
    assert "never-export-this-value" not in "\n".join(output.values())


def test_inventory_refuses_source_symlinks(tmp_path, monkeypatch):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "source.py").write_text("pass\n", encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    (root / "alias.py").symlink_to(outside / "source.py")
    _git_paths(monkeypatch, ["alias.py"])
    with pytest.raises(ValueError, match="source alias"):
        doc_inventory.collect(root)


def test_inventory_check_detects_drift_and_is_repeatable(tmp_path, monkeypatch, capsys):
    _git_paths(monkeypatch, ["module.py"])
    (tmp_path / "module.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(doc_inventory, "ROOT", tmp_path)
    assert doc_inventory.main(["--check"]) == 1
    assert "Regenerate with:" in capsys.readouterr().out
    assert doc_inventory.main([]) == 0
    assert doc_inventory.main(["--check"]) == 0
    index = tmp_path / "docs/high_signal_file_index.json"
    before = index.read_bytes()
    assert doc_inventory.main([]) == 0
    assert index.read_bytes() == before
    assert json.loads(before)[0]["exports"] == ["helper"]
    (tmp_path / "module.py").write_text("def renamed():\n    return 42\n", encoding="utf-8")
    assert doc_inventory.main(["--check"]) == 1
