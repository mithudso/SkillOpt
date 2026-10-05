## Default Execution Strategy

1. Read relevant files before editing.
2. Run tests after every change (`python -m pytest -q`).
3. Never invent commands or paths; verify against `pyproject.toml`, `scripts/`, `.github/workflows/ci.yml`, `docs/`.
4. Workflow log rule: after substantive changes append to `memory.md` and `prompts.md` with a version bump.

## Build, Test, and Validation Commands

```bash
pip install -e ".[dev]"
python -m pytest -q
ruff check skillopt skillopt_sleep skillopt_webui scripts tests   # not a CI gate
pip install -e ".[docs]" && python -m mkdocs build --strict
skillopt-sleep run --backend mock        # no credentials required
```

## High-level Architecture

- `skillopt/`: research loop. `engine/trainer.py` (ReflACTTrainer) runs rollout, reflect (`gradient/reflect.py`), aggregate (`gradient/aggregate.py`), select (`optimizer/clip.py`), update (`optimizer/skill.py`, `rewrite.py`), gate (`evaluation/gate.py`). Backends in `model/`, benchmarks in `envs/`.
- `skillopt_sleep/`: offline engine; `cycle.py` runs harvest, mine, replay, consolidate (gated), stage; `adopt` applies a staged proposal.
- `skillopt_webui/`: Gradio dashboard. `plugins/`: agent integrations.
- Details: `docs/ARCHITECTURE.md`, `docs/codebase-overview.md`.

## Key Conventions

1. Python >=3.10; ruff line length 120, rules E/F/I/W.
2. Tests are hermetic; live tests only with `SKILLOPT_TEST_REAL_OPENCODE=1`.
3. Fork of `microsoft/SkillOpt`: add new files only, do not edit upstream-tracked files.
4. Sync: `git fetch upstream && git merge upstream/main`.
5. Never commit `.env`, `.mcp.json`, `outputs/`, `.skillopt-sleep/`.
6. Sleep never changes live skills without `adopt` or explicit `--auto-adopt`.
7. New benchmark: copy `skillopt/envs/_template/`; new backend: `docs/guide/new-backend.md`.
8. Keep `memory.md` and `prompts.md` current.
