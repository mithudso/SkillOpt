# Known issues

Sources: grep of TODO/FIXME in code, `CHANGELOG.md`, tooling runs (2026-10-05). Nothing here is fixed by the bootstrap.

| # | Area | Issue | Where |
|---|---|---|---|
| 1 | Lint | `ruff check skillopt skillopt_sleep skillopt_webui scripts tests` reports 143 findings (111 auto-fixable); ruff is not a CI gate | `pyproject.toml [tool.ruff]` |
| 2 | Env registry | `scripts/train.py` registers `babyvision`, `mmrb`, `mathverse`, `sealqa`, `swebench` adapters that do not exist in `skillopt/envs/`; `except ImportError` hides it | `scripts/train.py` (`_register_builtin_envs`-style block, lines ~40-100) |
| 3 | Template | Only TODOs in code are the intentional placeholders in `skillopt/envs/_template/env_template.py:4,105` | |
| 4 | OpenClaw | Reference adaptation is not directly runnable (environment-specific absolute paths, Python 3.10 syntax and backend-factory gaps, per its README) | `plugins/openclaw/README.md` |
| 5 | Docs drift | `docs/reference/cli.md` notes PyPI 0.2.0 lacks features on `main` (openai_compatible, handoff, cursor/pi/opencode, multi-skill) | `docs/reference/cli.md` |
| 6 | `.env.example` | Lists only a subset of the ~130 env vars read in code | `.env.example`; full list in `docs/DEVELOPMENT.md` |
| 7 | Dependency pin | `requirements.txt` comments `gradio>=4.0.0` but `pyproject.toml` webui extra requires `>=5.50.0,<7` | `requirements.txt`, `pyproject.toml` |
| 8 | Packaging | `[tool.setuptools.package-data]` includes only `*.md`; `skillopt/envs/*/skills`, YAML configs are not packaged (TODO: verify wheel contents) | `pyproject.toml` |
| 9 | CI | No lint, type-check, or coverage job | `.github/workflows/ci.yml` |
| 10 | Usage accounting | Copilot CLI backends report no token counts (usage totals are zero) | `CHANGELOG.md` Unreleased |

See `CHANGELOG.md` `[Unreleased]` for recent behavior changes and caveats.
