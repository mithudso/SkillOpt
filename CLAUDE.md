# CLAUDE.md — SkillOpt (fork)

Fork of `microsoft/SkillOpt` (Python package `skillopt` v0.2.0). Two products in one repo:

- **SkillOpt** (`skillopt/`): research training loop that optimizes a natural-language skill document (rollout → reflect → aggregate → select → update → evaluate/gate) on benchmarks.
- **SkillOpt-Sleep** (`skillopt_sleep/`): offline "sleep cycle" engine that harvests agent session transcripts, mines recurring tasks, replays them, and stages gate-validated edits to `CLAUDE.md`/`SKILL.md`. No runtime dependency on `skillopt/`.

## Repository shape

| Path | What |
|---|---|
| `skillopt/` | research package: `engine/trainer.py` (ReflACTTrainer), `gradient/`, `optimizer/`, `evaluation/gate.py`, `model/` (backends), `envs/` (benchmarks), `prompts/*.md` |
| `skillopt_sleep/` | Sleep engine: `cycle.py` orchestrator, `harvest*.py`, `mine.py`, `replay.py`, `consolidate.py`, `gate.py`, `staging.py`, `backend.py`, `evalkit.py` |
| `skillopt_webui/` | Gradio dashboard (`app.py`) |
| `scripts/` | CLI entry points `train.py`, `eval_only.py`, data prep, benchmark launchers |
| `plugins/` | agent integrations (Claude Code, Codex, Copilot, Cursor, Devin, DeepSeek Harness, OpenClaw) — see `AGENTS.md` |
| `configs/` | YAML run configs (`_base_/default.yaml`, per-benchmark, `features/`) |
| `data/`, `ckpt/` | benchmark splits / reference checkpoints |
| `tests/` | pytest suite (hermetic) |
| `docs/` | mkdocs site content + bootstrap docs (see below) |

Full map: `docs/codebase-overview.md`. Architecture: `docs/ARCHITECTURE.md`.

## Commands (verified against `pyproject.toml`, `.github/workflows/ci.yml`, `CONTRIBUTING.md`)

```bash
pip install -e ".[dev]"                 # core + ruff + pytest (CI install)
pip install -e ".[webui]"               # Gradio dashboard (gradio>=5.50.0,<7)
pip install -e ".[docs]"                # mkdocs-material
python -m pytest -q                     # full suite (CI: py3.10/3.11/3.12)
python -m pytest tests/test_webui_build_gradio.py tests/test_webui_env_preflight.py -q   # needs gradio extra
ruff check skillopt skillopt_sleep skillopt_webui scripts tests   # configured in pyproject; NOT a CI gate; currently 143 findings
python -m mkdocs build --strict         # CI docs gate
python -m mkdocs serve                  # preview
skillopt-train --config configs/searchqa/default.yaml --out_root outputs/run   # == python scripts/train.py
skillopt-eval  --config <cfg.yaml> --skill <skill.md> [--split valid_unseen]    # == python scripts/eval_only.py
skillopt-sleep run --backend mock       # == python -m skillopt_sleep ; mock needs no credentials
python -m skillopt_webui                # dashboard, --port 7860 default
```

Sleep subcommands: `run`, `dry-run`, `status`, `adopt`, `harvest`, `schedule`, `unschedule`, `evalkit` (paired A/B; also `python -m skillopt_sleep.evalkit`). Env vars: see `.env.example` and `docs/DEVELOPMENT.md`.

## Conventions

- Python >=3.10, ruff line-length 120, rules `E,F,I,W` (E501 ignored). Type hints on signatures; concise docstrings.
- Tests must be hermetic: live-backend tests are opt-in via `SKILLOPT_TEST_REAL_OPENCODE=1` / `SKILLOPT_TEST_REAL_OPENCODE_SOURCE=1`.
- Never commit `.env`, `.mcp.json`, `outputs/`, `.skillopt-sleep/` (all gitignored). Never write credentials into docs.
- Sleep safety: proposals are staged; nothing live changes until `adopt` (or explicit `--auto-adopt`).
- New benchmark: copy `skillopt/envs/_template/`, register lazily in `scripts/train.py` and `scripts/eval_only.py`. New backend: follow `docs/guide/new-backend.md`.
- Never invent commands/paths; unknown means `TODO: find in <where>`.

## Fork workflow

- `origin` = `https://github.com/mithudso/SkillOpt.git`, `upstream` = `https://github.com/microsoft/SkillOpt.git`.
- Sync: `git fetch upstream && git merge upstream/main`.
- Keep fork-only changes **additive** (new files only; do not edit upstream-tracked files such as `README.md`, `CONTRIBUTING.md`, `mkdocs.yml`, `docs/guide/*`, source, tests, workflows) so merges stay conflict-free.
- Fork-only files: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `memory.md`, `prompts.md`, `.github/copilot-instructions.md`, `.editorconfig`, `.gitattributes`, `llms*.txt`, `docs/{ARCHITECTURE,DEVELOPMENT,COMPONENTS,TESTING,INSTALLATION,known-issues,external-calls,integrations-and-assumptions,logging,onboarding,codebase-overview}.md`, `docs/high_signal_file_index.json`, `docs/repo-bootstrap-audit-*.md`, `.stele/project.json` (Stele binding to project `skillopt-ocj5r`), plus the generic skill-optimization env: `skillopt/envs/skilltask/`, `scripts/skillopt_skill.py`, `configs/skilltask/default.yaml`, `tests/test_skilltask_env.py`.

## Optimizing an arbitrary skill (fork-only)

`skilltask` trains any Markdown skill against a task set (`{"id", "input", "expected"|"rubric"}` per JSONL line; graded by `contains`/`exact` match or an LLM judge on the optimizer backend). Launch through `scripts/skillopt_skill.py train|eval` — it registers `skilltask` in the lazy registries of `scripts/train.py` / `scripts/eval_only.py` without editing them, and defaults `CLAUDE_SETTING_SOURCES=project` so the user's Claude Code hooks do not leak into `claude_chat` rollouts. The `skillopt-run` skill (`/Users/mitch/.claude/skills/skillopt-run/SKILL.md`) drives the whole flow.

## Workflow log rule

After every substantive change: append a new version section to `memory.md` (what was done, next steps) and append the user's request verbatim to `prompts.md` (same version number). Bump the fork log version (`vN.M`); this is independent of the package version.

## Pointers

- LLM-oriented index: `llms.txt` (repo root, maintained separately).
- Human docs: `docs/` (`docs/guide/`, `docs/reference/`, `docs/sleep/`), plus the bootstrap suite listed above.
