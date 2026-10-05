# Development

## Setup
```bash
git clone https://github.com/mithudso/SkillOpt.git && cd SkillOpt
git remote add upstream https://github.com/microsoft/SkillOpt.git   # if absent
pip install -e ".[dev]"
```
Optional extras: `.[webui]`, `.[docs]`, `.[claude]`, `.[qwen]`, `.[alfworld]`, `.[searchqa]`.

## Commands
| Task | Command |
|---|---|
| Tests | `python -m pytest -q` |
| Lint | `ruff check skillopt skillopt_sleep skillopt_webui scripts tests` (not in CI) |
| Docs | `python -m mkdocs serve` / `python -m mkdocs build --strict` |
| Train | `skillopt-train --config configs/searchqa/default.yaml` (needs data: `python scripts/materialize_searchqa.py`, see `docs/guide/first-experiment.md`) |
| Eval | `skillopt-eval --config <cfg> --skill <skill.md> --split valid_unseen` |
| Sleep | `skillopt-sleep run --backend mock` ; `status`; `adopt`; `schedule --hour 3 --minute 17` |
| WebUI | `python -m skillopt_webui --port 7860` |
| Benchmark launchers | `scripts/run_alfworld.sh`, `scripts/run_searchqa.sh`, `scripts/run_spreadsheetbench.sh` (TODO: read each for required env) |

## Workflow
1. Branch or work on `main` of the fork; keep changes additive vs upstream.
2. Make changes, run focused tests then the full suite.
3. Append `memory.md` and `prompts.md` entries.
4. Sync upstream: `git fetch upstream && git merge upstream/main`.

Extending: new benchmark -> `skillopt/envs/_template/` + register in `scripts/train.py` and `scripts/eval_only.py`; new backend -> `docs/guide/new-backend.md`; new Sleep source -> `skillopt_sleep/harvest_<name>.py` + `harvest_sources.py`.

## Environment variables (read in code; placeholders only)
Only a subset appears in `.env.example`. Full inventory by area (verified by grep of `os.environ`/`os.getenv`):
- Azure OpenAI: `AZURE_OPENAI_{ENDPOINT,API_KEY,API_VERSION,AUTH_MODE,DEPLOYMENT,MANAGED_IDENTITY_CLIENT_ID}`; role-scoped variants `AZURE_OPENAI_{OPTIMIZER,TARGET}_*`, `{OPTIMIZER,TARGET}_AZURE_OPENAI_*`, `{OPTIMIZER,TARGET}_DEPLOYMENT`, `{OPTIMIZER,TARGET}_BACKEND`; `*_AD_SCOPE`.
- Backend routing: `REFLACT_MODEL_BACKEND`, `REFLACT_{CLAUDE,CODEX}_TRACE_TO_OPTIMIZER`.
- OpenAI-compatible: `OPENAI_COMPATIBLE_{BASE_URL,API_KEY,MODEL,TEMPERATURE,MAX_TOKENS,TIMEOUT_SECONDS}`, `DEEPSEEK_{BASE_URL,API_KEY}`.
- Qwen: `QWEN_CHAT_{BASE_URL,MODEL,API_KEY,TEMPERATURE,MAX_TOKENS,TIMEOUT_SECONDS,THINKING_MODE,ENABLE_THINKING,USE_MAX_COMPLETION_TOKENS}`.
- MiniMax: `MINIMAX_{API_KEY,BASE_URL,REGION,TIMEOUT_SECONDS,TEMPERATURE,MAX_TOKENS,ENABLE_THINKING}`.
- Claude: `CLAUDE_CLI_BIN`, `ANTHROPIC_API_KEY`, `CLAUDE_CODE_EXEC_{PATH,PROFILE,USE_SDK,EFFORT,MAX_THINKING_TOKENS}`, `CLAUDE_{PERMISSION_MODE,SETTING_SOURCES,ALLOW_ATTACHMENT_READ}`, `SKILLOPT_CLAUDE_BIN`.
- Codex: `CODEX_{CLI_BIN,PATH,PROFILE,SANDBOX,SANDBOX_MODE,WORKING_DIRECTORY}`, `CODEX_EXEC_{PATH,PROFILE,SANDBOX,USE_SDK,FULL_AUTO,APPROVAL_POLICY,NETWORK_ACCESS,WEB_SEARCH,REASONING_EFFORT}`, `EXEC_EMPTY_RESPONSE_RETRIES`.
- Copilot: `COPILOT_{CHAT_TIMEOUT,CHAT_OPTIMIZER_MODEL,CHAT_TARGET_MODEL,AVAILABLE_TOOLS}`, `COPILOT_EXEC_{PATH,HOME,ALLOW_ALL_TOOLS}`.
- Cursor: `CURSOR_EXEC_{PATH,SANDBOX}`.
- Benchmarks: `ALFWORLD_DATA`, `ALFWORLD_WORKER_START_METHOD`, `OFFICEQA_DOCS_DIR`, `OFFICEQA_SEARCH_API_URL`.
- Sleep: `SKILLOPT_SLEEP_{WORKERS,REPO,HANDOFF_DIR,PROMPTS_PATH,AGENT_MARKERS,COMPAT_MAX_TOKENS,CHAT_EXTRA_BODY}`, `SKILLOPT_SLEEP_{CLAUDE,CODEX,COPILOT,CURSOR,OPENCODE,PI}_MODEL`, `SKILLOPT_SLEEP_{CODEX,COPILOT,CURSOR,OPENCODE}_PATH`, `SKILLOPT_SLEEP_COPILOT_{HOME,FULL_ENV}`, `OPENCODE_DB`.
- Superpowers/Devin/judge: `SKILLOPT_UNSAFE`, `SKILLOPT_{REPO,RUN_TIMEOUT,ATTEMPT,JUDGE,JUDGE_MODEL,HOST_AUTH,INHERIT_PATH}`, `SKILLOPT_DEVIN_{WORKSPACES,CLAUDE_HOME}`.
- Tests: `SKILLOPT_TEST_REAL_OPENCODE`, `SKILLOPT_TEST_REAL_OPENCODE_SOURCE`.

## Troubleshooting
- `ModuleNotFoundError: gradio` -> `pip install -e ".[webui]"`.
- Env missing from `train.py --config ...` -> its adapter import failed silently; install the extra (e.g. `.[alfworld]`) and check `_ENV_REGISTRY` in `scripts/train.py`.
- Windows console `UnicodeEncodeError` is mitigated by `skillopt/utils/console.py`.
