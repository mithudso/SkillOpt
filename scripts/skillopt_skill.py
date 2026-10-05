#!/usr/bin/env python3
"""Train or evaluate an arbitrary skill document with the ``skilltask`` env.

Fork-local launcher. It registers ``skilltask`` in the lazy env registries of
``scripts/train.py`` and ``scripts/eval_only.py`` without editing them, then
hands the remaining arguments to the chosen entry point.

    python scripts/skillopt_skill.py train --config <run>/config.yaml --out_root <run>/out
    python scripts/skillopt_skill.py eval  --config <run>/config.yaml --skill <run>/out/best_skill.md
"""
from __future__ import annotations

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

USAGE = "usage: skillopt_skill.py {train|eval} [train.py / eval_only.py arguments]"


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in {"train", "eval"}:
        sys.exit(USAGE)
    mode = sys.argv.pop(1)

    # claude_chat shells out to `claude -p`. Loading the user's settings would
    # run their hooks and output styles inside every rollout, so default to
    # project-only settings (the CLI runs in an empty temp dir).
    os.environ.setdefault("CLAUDE_SETTING_SOURCES", "project")

    from skillopt.envs.skilltask.adapter import SkillTaskAdapter

    if mode == "train":
        from scripts import train as entry
    else:
        from scripts import eval_only as entry
    entry._register_builtins()
    entry._ENV_REGISTRY["skilltask"] = SkillTaskAdapter
    original = entry._register_builtins

    def _register_with_skilltask() -> None:
        original()
        entry._ENV_REGISTRY["skilltask"] = SkillTaskAdapter

    entry._register_builtins = _register_with_skilltask
    entry.main()


if __name__ == "__main__":
    main()
