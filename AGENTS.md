# AGENTS.md — SkillOpt (fork)

Rules for Codex and other coding agents. Same rules as `CLAUDE.md`; this file adds the integration catalog.

## Rules

1. Read relevant files before editing; never invent commands or paths (verify in `pyproject.toml`, `scripts/`, `.github/workflows/ci.yml`, `docs/`).
2. Setup/test: `pip install -e ".[dev]"`, then `python -m pytest -q`. Docs: `python -m mkdocs build --strict` (needs `.[docs]`). Lint: `ruff check skillopt skillopt_sleep skillopt_webui scripts tests` (not a CI gate).
3. Fork workflow: `origin` = `https://github.com/mithudso/SkillOpt.git`, `upstream` = `https://github.com/microsoft/SkillOpt.git`; sync with `git fetch upstream && git merge upstream/main`. Add new files only; do not edit upstream-tracked files.
4. Workflow log: append to `memory.md` and `prompts.md` with a version bump after each substantive change.
5. Never commit secrets, `.env`, `.mcp.json`, `outputs/`, `.skillopt-sleep/`.
6. Tests are hermetic; live tests require `SKILLOPT_TEST_REAL_OPENCODE=1`.
7. See `CLAUDE.md` for layout, `docs/ARCHITECTURE.md` for design, `llms.txt` for the LLM index.

## Agent-facing integrations (`plugins/`, SkillOpt-Sleep)

All wrap the shared `skillopt_sleep` engine (`skillopt-sleep` CLI / `python -m skillopt_sleep`). Overview: `plugins/README.md`.

| Platform | Path | Mechanism | Notes |
|---|---|---|---|
| Claude Code | `plugins/claude-code/` | marketplace plugin: commands `skillopt-sleep`, `skillopt-sleep-handoff`; skill; `hooks/on-session-end.sh`; `scripts/install-cron.sh` | installable |
| Codex | `plugins/codex/` | user-level skill + `install.sh`/`install.ps1` | installable |
| Cursor | `plugins/cursor/` (+ `.cursor-plugin/marketplace.json`) | native command + skill; no hooks/MCP | installable |
| GitHub Copilot | `plugins/copilot/` | stdlib MCP server `mcp_server.py` (7 `sleep_*` tools), `copilot-instructions.snippet.md` | MCP |
| Devin | `plugins/devin/` | MCP server + `harvest_devin.py` transcript converter, `judge.py` | MCP |
| DeepSeek Harness (dsh) | `plugins/dsh/` | Cordis plugin (Node, `package.json`), 7 `skillopt_*` tools + skill | npm dependabot configured |
| OpenClaw | `plugins/openclaw/` | contributed reference adaptation | README says not directly runnable; treat as porting material |

Launch helpers: `plugins/run-sleep.sh`, `plugins/run-sleep.ps1`, `plugins/run-sleep.cmd`.

Backends the engine can drive (`--backend`): `mock`, `claude`, `codex`, `copilot`, `cursor`, `pi`, `opencode`, `handoff`, `azure_openai`. Transcript sources include Claude, Codex, Copilot (VS Code and CLI), Cursor, Pi, OpenCode (`skillopt_sleep/harvest_*.py`).

Env/auth dependencies per backend: see `docs/integrations-and-assumptions.md`.
