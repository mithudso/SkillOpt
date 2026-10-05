# Codebase overview

File map grouped by top-level directory (every top-level entry is covered).

## Root files
- `pyproject.toml` package metadata, extras, console scripts, ruff config. `requirements.txt` plain pip list. `mkdocs.yml` docs site config. `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`. `index.html`, `skillopt.html` project landing pages. `.env.example` env template. `.gitignore`.
- Fork bootstrap: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `memory.md`, `prompts.md`, `.editorconfig`, `.gitattributes`.

## `skillopt/` research package
- `config.py`, `types.py`, `__init__.py`.
- `engine/trainer.py` ReflACTTrainer (epoch/step loop, history, state, gate wiring).
- `gradient/` `reflect.py`, `aggregate.py`.
- `optimizer/` `clip.py` (select), `scheduler.py`, `lr_autonomous.py`, `skill.py` (apply patches), `rewrite.py`, `update_modes.py`, `appendix.py`, `skill_aware.py`, `slow_update.py`, `meta_skill.py`.
- `evaluation/gate.py` accept/reject.
- `scheduler/` package placeholder. `datasets/base.py`.
- `model/` `router.py`, `common.py`, `backend_config.py`, `azure_openai.py`, `openai_compatible_backend.py`, `claude_backend.py`, `claude_code_backend.py`, `codex_backend.py`, `codex_harness.py`, `copilot_backend.py`, `qwen_backend.py`, `minimax_backend.py`.
- `envs/` `base.py` + `alfworld/`, `docvqa/`, `livemathematicianbench/`, `officeqa/`, `searchqa/`, `spreadsheetbench/`, `_template/`.
- `prompts/*.md` analyst, merge, ranking, rewrite, slow-update, meta-skill, LR prompts.
- `utils/` `scoring.py`, `json_utils.py`, `console.py`.

## `skillopt_sleep/` Sleep engine
- Orchestration: `__main__.py` (CLI), `cycle.py`, `config.py`, `state.py`, `budget.py`, `scheduler.py`, `types.py`.
- Harvest: `harvest.py`, `harvest_{codex,copilot,copilot_cli,cursor,opencode,pi}.py`, `harvest_sources.py`.
- Mine/replay/judge: `mine.py`, `llm_miner.py`, `tasks_file.py`, `replay.py`, `rollout.py`, `judges.py`, `prompts.py`.
- Consolidate/gate/stage: `consolidate.py`, `dream.py`, `slow_update.py`, `multi_skill.py`, `gate.py`, `staging.py`, `skill_resolver.py`, `memory.py`, `evidence.py`.
- Backends: `backend.py`, `handoff_backend.py`. Stats: `evalkit.py`.
- `adapters/superpowers.py`; `experiments/` (persona, gbrain, transfer, sweep runners).

## `skillopt_webui/`
`app.py` Gradio dashboard, `__main__.py` launcher.

## `scripts/`
`train.py`, `eval_only.py`, `materialize_searchqa.py`, `run_alfworld.sh`, `run_searchqa.sh`, `run_spreadsheetbench.sh`, `smoke_superpowers.sh`.

## `plugins/`
`README.md`, `run-sleep.{sh,ps1,cmd}`; `claude-code/`, `codex/`, `copilot/`, `cursor/`, `devin/`, `dsh/` (Node), `openclaw/`. See `AGENTS.md`.

## `configs/`
`_base_/default.yaml`, `features/soft_gate.yaml`, per-benchmark dirs (`alfworld`, `docvqa`, `livemathematicianbench`, `officeqa`, `searchqa`, `spreadsheetbench`).

## `data/` and `ckpt/`
`data/*_split/` tracked id splits per benchmark, `data/README.md`; `ckpt/<bench>/` reference checkpoints, `ckpt/README.md`.

## `tests/`
~85 pytest files plus `fixtures/` and `test_runners.Tests.ps1`; see `docs/TESTING.md`.

## `docs/`
Upstream: `index.md`, `guide/`, `reference/{api,cli,config}.md`, `sleep/`, `superpowers/`, `contributing.md`, `review_guidelines.md`, `guideline.html`. Fork bootstrap: `ARCHITECTURE.md`, `DEVELOPMENT.md`, `COMPONENTS.md`, `TESTING.md`, `INSTALLATION.md`, `known-issues.md`, `external-calls.md`, `integrations-and-assumptions.md`, `logging.md`, `onboarding.md`, `codebase-overview.md`, `high_signal_file_index.json`, `repo-bootstrap-audit-2026-10-05.md`.

## `.github/`
`workflows/ci.yml` (test, webui, docs), `dependabot.yml` (pip, npm in `plugins/dsh`, github-actions); fork adds `copilot-instructions.md`.

## Other top-level dirs
- `.cursor-plugin/marketplace.json` Cursor marketplace manifest pointing at `plugins/cursor`.
- `.remember/` local tool state (logs, tmp, install marker) from the Remember plugin; not project code.
- `blog/` static blog page (`gating-reflection-safe-updates`, `index.html`).
- `skillopt-assets/` images/logos used by README and site.
