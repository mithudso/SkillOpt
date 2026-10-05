# Testing

## Suites
- `tests/` (pytest, `tests/__init__.py`): ~85 `test_*.py` files, hermetic, no network. No `[tool.pytest]` config in `pyproject.toml` (defaults apply).
  - Sleep engine: `test_sleep_*.py`, `test_gate*.py`, `test_evalkit.py`, `test_harvest_*.py`, `test_scheduler*.py`, `test_handoff_backend.py`, `test_staging_redaction_azure.py`.
  - Research loop: `test_aggregate_fallback.py`, `test_holdout_integrity.py`, `test_split_*.py`, `test_trainer_failure_patterns.py`, `test_unmatched_edits*.py`, `test_scoring.py`, `test_json_utils.py`, `test_types.py`.
  - Backends: `test_*_backend*.py`, `test_azure_openai_compat.py`, `test_openai_compatible_backend.py`, `test_minimax_*.py`, `test_qwen_backend.py`, `test_role_backend_resolution.py`.
  - Envs: `test_alfworld_paths.py`, `test_searchqa_rollout_failfast.py`, `test_materialize_searchqa.py`, `test_react_agent_no_shell.py`, `test_data_manifests.py`.
  - Plugins/MCP: `test_plugin_sync.py`, `test_devin_plugin.py`, `test_mcp_schema.py`, `test_run_sleep_fallback.py`, `test_superpowers_scenarios.py`, `test_systematic_debugging_*.py`, `test_runners.Tests.ps1` (Pester, not collected by pytest).
  - WebUI: `test_webui_*.py` (importorskip gradio).
  - Live (opt-in): `test_backend_opencode_live.py`, `test_harvest_opencode_live.py` gated on `SKILLOPT_TEST_REAL_OPENCODE=1` / `SKILLOPT_TEST_REAL_OPENCODE_SOURCE=1`.
- `plugins/openclaw/tests/`: not run by CI (TODO: verify whether collected by `pytest`).
- Fixtures: `tests/fixtures/{copilot,evalkit}`.

## Commands
```bash
pip install -e ".[dev]"
python -m pytest -q
python -m pytest tests/test_gate.py -q                 # focused
pip install -e ".[dev]" "gradio==5.50.0" && python -m pytest tests/test_webui_build_gradio.py tests/test_webui_env_preflight.py -q
python -m mkdocs build --strict                        # needs .[docs]
```

## CI gates (`.github/workflows/ci.yml`, on push/PR to `main`)
1. `test`: Python 3.10/3.11/3.12, `pip install -e ".[dev]"`, `python -m pytest -q` with live-test env vars set to `"0"`.
2. `webui`: Python 3.11, gradio 5.50.0 and 6.26.0, runs the two webui test files.
3. `docs`: `pip install -e ".[docs]"`, `mkdocs build --strict`.
Ruff is configured but not run in CI. No coverage tool or numeric coverage threshold is enforced.

## Coverage target
Meaningful coverage of changed/risky paths with real behavioral assertions (including logs where relevant); no blanket line-coverage mandate. Enforced numeric gate: none (TODO: decide whether to add `pytest-cov`).
