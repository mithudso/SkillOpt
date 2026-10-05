# Integrations and assumptions

## External services
| Service | Used by | Auth |
|---|---|---|
| Azure OpenAI / OpenAI | `skillopt/model/azure_openai.py`, Sleep `azure_openai` backend | `AZURE_OPENAI_API_KEY`, `azure_cli` (`az login`), or managed identity (`AZURE_OPENAI_AUTH_MODE`) |
| OpenAI-compatible endpoints (DeepSeek, Novita, etc.) | `openai_compatible` backend | `OPENAI_COMPATIBLE_{BASE_URL,API_KEY,MODEL}` |
| Qwen via vLLM/SGLang | `qwen_chat` | `QWEN_CHAT_BASE_URL`, optional key |
| MiniMax | `minimax_chat` | `MINIMAX_API_KEY`, `MINIMAX_REGION` (`global_en`/`cn_zh`) |
| Claude Code CLI | `claude_chat`, `claude_code_exec`, Sleep `claude` | CLI's own login or `ANTHROPIC_API_KEY`; no direct Anthropic client |
| Codex CLI | `codex`, `codex_exec`, Sleep `codex` | CLI login |
| GitHub Copilot CLI | `copilot_chat`, `copilot_exec`, Sleep `copilot` | CLI sign-in; `copilot_exec_allow_all_tools` is explicit opt-in |
| Cursor Agent CLI | `cursor_exec`, Sleep `cursor` | CLI login |
| Pi, OpenCode CLIs | Sleep `pi`, `opencode` | CLI login; OpenCode history via local SQLite (`OPENCODE_DB`) |
| OfficeQA search API | `skillopt/envs/officeqa` | `OFFICEQA_SEARCH_API_URL` |
| GitHub Pages / mkdocs | docs site `https://microsoft.github.io/SkillOpt` | upstream-owned |

## Assumptions
- Python >=3.10; Linux/macOS/Windows supported (Windows helpers: `plugins/run-sleep.ps1`, `.cmd`, `scheduler.py` schtasks).
- Sleep reads local transcripts from each agent's home dir (e.g. `~/.claude`, `~/.codex`, `~/.cursor`, `~/.pi`) unless overridden via `--*-home` flags.
- Research benchmarks need external datasets under `data/` (splits are tracked; raw data is not) and some need extra installs (alfworld, vllm, datasets).
- Fork assumption: upstream-tracked files are never edited here.
- Plugins dsh needs Node (own `package.json`); the rest are Python/shell.
- Model-written code runs in subprocesses for SpreadsheetBench (`skillopt/envs/spreadsheetbench/executor.py`): treat as untrusted-code execution.

## Environment differences
- CI sets `SKILLOPT_TEST_REAL_OPENCODE=0` and `SKILLOPT_TEST_REAL_OPENCODE_SOURCE=0`.
- Local-only paths ignored by git: `.env`, `.mcp.json`, `configs/local/`, `outputs/`, `.skillopt-sleep/`.
