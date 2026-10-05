# Repo bootstrap audit — 2026-10-05

Scope: `update_to_ideal_repo` on the `mithudso/SkillOpt` fork of `microsoft/SkillOpt` (Python). Constraint: additive only (no edits to upstream-tracked files), so gaps in tracked files are reported, not fixed. No prior `docs/repo-bootstrap-audit-*.md` existed (no retracted findings).

## Audit table

| File | Exists | Missing | Action |
|---|---|---|---|
| `.github/copilot-instructions.md` | created | - | Created (4 sections, starts with `## Default Execution Strategy`) |
| `CLAUDE.md` | created | - | Created |
| `AGENTS.md` | created | no `.claude/agents/` or `.github/agents/` exist; catalog is of `plugins/` integrations | Created |
| `GEMINI.md` | created | Gemini tool mappings | Created minimal pointer |
| `memory.md`, `prompts.md` | created | - | Created at v0.1 |
| `docs/archive/` + `scripts/rotate-workflow-logs.mjs` | no | both | N/A now (Node tool; logs small) |
| `.editorconfig` | created | - | Created |
| `.gitignore` | yes | - | OK (covers env, outputs, sleep state) |
| `.gitattributes` | created | - | Created |
| `.nvmrc`/`.node-version` | no | - | N/A (Python repo; `plugins/dsh` is Node, TODO: pin there if wanted) |
| `.tool-versions` | no | - | Optional, skipped |
| `.env.example` | yes (tracked) | ~120 of ~130 env vars read in code are absent | Not edited (tracked upstream file); inventory in `docs/DEVELOPMENT.md` |
| `.vscode/*`, `.mcp.json` | no | all | Skipped (`.mcp.json` is gitignored by upstream; no MCP server dev config needed) |
| `.github/workflows/*.yml` | yes (`ci.yml`) | lint/type-check/coverage jobs | TODO |
| `.github/dependabot.yml` | yes | - | OK |
| `.github/CODEOWNERS`, `PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/*` | no | all | Not created (upstream-owned governance; TODO if fork needs them) |
| `.github/SECURITY.md` | no | root `SECURITY.md` exists | Not created |
| `LICENSE`, `CONTRIBUTING.md` | yes | CONTRIBUTING lacks link to `docs/DEVELOPMENT.md` | Not edited |
| `CODE_OF_CONDUCT.md` | no | file | TODO |
| `docs/ARCHITECTURE.md` | created | - | Created with mermaid + ADRs |
| `docs/DEVELOPMENT.md` | created | - | Created |
| `docs/COMPONENTS.md` | created | - | Created |
| `docs/SECURITY.md` | no | threat model | TODO (`docs/superpowers/SECURITY.md` and root `SECURITY.md` exist) |
| `docs/MCP.md` | no | MCP docs | TODO (`plugins/copilot`, `plugins/devin` ship MCP servers; documented in their READMEs) |
| `docs/TESTING.md` | created | numeric coverage gate (none enforced) | Created |
| `README.md` | yes | - | OK, not edited |
| `docs/codebase-overview.md` | created | - | Created, covers every top-level dir |
| `docs/high_signal_file_index.json` | created | - | 67 entries, all paths verified to exist |
| `scripts/semantic_indexer.py`, `scripts/watch_and_index.sh` | no | both | Skipped (hub-specific, not in this repo's scope) |
| `scripts/check-doc-indexes.mjs` (or equivalent) | no | index path checker + CI wiring | TODO (could be a Python script) |
| `docs/integrations-and-assumptions.md` | created | - | Created |
| `docs/known-issues.md` | created | - | Created |
| `docs/onboarding.md` | created | - | Created |
| `docs/INSTALLATION.md` | created | - | Created (summarizes `docs/guide/installation.md`) |
| `docs/requirements.md` | no | file | TODO |
| `docs/logging.md` | created | - | Created |
| `docs/caching-and-optimization.md` | no | file | TODO (no cache layer inventoried beyond Azure token cache and trainer rollout cache) |
| `docs/runbooks/*.md` | no | all | TODO |
| `docs/external-calls.md` | created | per-call test mapping, some retry cells | Created |
| `llms*.txt` | n/a | - | Owned by another agent |

## N/A (Node-only / out of scope)
`operations-registry.js`, `scripts/generate-ops-registry-doc.mjs`, `ops:doc`/`ops:doc:check`, `docs/operations-registry.json`, `docs/tool-inventory.json`, CI drift check, `.nvmrc`, `package.json` scripts: N/A, Python repo with no operations registry. 5-standard auto-remediation contract: not applicable.
Customer-data-in-VCS check: no customer data observed in the top-level tree (not exhaustively scanned). Chrome-extension, native-host, offscreen checks: N/A.

## Remaining TODOs (code findings not fixed)
1. `ruff check skillopt skillopt_sleep skillopt_webui scripts tests` -> 143 findings (111 auto-fixable); add as CI gate after cleanup.
2. `scripts/train.py` registers non-existent envs (`babyvision`, `mmrb`, `mathverse`, `sealqa`, `swebench`) behind silent `except ImportError`.
3. `.env.example` documents a small subset of env vars (see `docs/DEVELOPMENT.md`).
4. `requirements.txt` says `gradio>=4.0.0`, `pyproject.toml` requires `>=5.50.0,<7`.
5. Retry/timeouts and logging are inconsistent across backends; no `logging` setup in the research loop; no log assertions in tests.
6. `pyproject.toml` package-data only includes `*.md` (verify wheel includes seed skills/configs).
7. `plugins/openclaw` is not runnable as shipped (per its README).
8. Add `CODEOWNERS`, PR/issue templates, `CODE_OF_CONDUCT.md`, `docs/SECURITY.md`, `docs/MCP.md`, `docs/requirements.md`, `docs/runbooks/` if the fork wants full standard.
9. Index checker (`check-doc-indexes` equivalent) not present; `docs/high_signal_file_index.json` can rot.
10. code-deep-optimizer pass not run (out of scope for this additive pass); crawl-repo-to-llms output owned by another agent; hub registration and commit left to the parent.
