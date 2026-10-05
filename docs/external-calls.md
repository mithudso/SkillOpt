# External calls

Inventory of every LLM / HTTP / subprocess call (grep-derived, 2026-10-05; line numbers drift). "Logger" = how failures surface. The code base mostly uses `print` and exceptions; only `skillopt_sleep/backend.py` uses `logging.getLogger("skillopt_sleep")`. No tests are mapped per call (TODO: map).

## LLM / HTTP

| file:line | Target | Retry / timeout | Logging |
|---|---|---|---|
| `skillopt/model/azure_openai.py:415,504` (`client.chat.completions.create`) | Azure OpenAI or OpenAI (`AZURE_OPENAI_*`) | `retries=5` default, backoff `min(2**attempt, 30)`s; raises `RuntimeError("LLM call failed after N retries")` | print / exception |
| `skillopt/model/azure_openai.py:264` (`subprocess.check_output az account get-access-token`) | Azure CLI (token for `azure_cli` auth) | token cached; refresh when <300s left | exception |
| `skillopt/model/openai_compatible_backend.py:114,200` | any OpenAI-compatible `/v1` endpoint (`OPENAI_COMPATIBLE_*`) | TODO: read retry loop | print / exception |
| `skillopt/model/qwen_backend.py:254` (`urllib.request.urlopen`) | Qwen/vLLM endpoint (`QWEN_CHAT_BASE_URL`) | `retries=5`, backoff `min(2**attempt,30)` | exception |
| `skillopt/model/minimax_backend.py:183` (`urlopen`) | MiniMax API (`MINIMAX_BASE_URL`/region) | `retries=5`, timeout `MINIMAX_TIMEOUT_SECONDS` | exception |
| `skillopt/envs/spreadsheetbench/codegen_agent.py:196,428` | Azure/OpenAI chat via `_llm_call_with_retry` | 5 tries, `min(2**attempt+rand,60)`s, 120s timeout | exception |
| `skillopt/envs/officeqa/tool_runtime.py:481` (`urlopen`) | `OFFICEQA_SEARCH_API_URL` custom search | `max_retries` param; retries on retryable HTTP / connection errors | RuntimeError messages |
| `skillopt_sleep/backend.py:2380` (`AzureOpenAIBackend`), `:2319,2340,2461` | Azure/OpenAI (Sleep `azure_openai` backend, responses API variant) | TODO: read | `logging.getLogger("skillopt_sleep")` warnings (`:2279,2295`) |
| `plugins/openclaw/skillopt_sleep_openclaw.py:57,75` | DeepSeek/Ollama OpenAI-style endpoint | 180s / 30s timeout, no retry | exception |
| `plugins/devin/judge.py:97` | judge LLM HTTP endpoint | 30s timeout | TODO |

## Subprocess (agent CLIs and OS tools)

| file:line | Target | Timeout | Logging |
|---|---|---|---|
| `skillopt/model/claude_backend.py:278` | `claude` CLI (`CLAUDE_CLI_BIN`) | `timeout or 300` | exception |
| `skillopt/model/codex_backend.py:338` | Codex CLI | `TimeoutExpired` handled `:467` | exception |
| `skillopt/model/codex_harness.py:931,1177,1385,1813,1933` | codex / claude-code / cursor / copilot exec harnesses (+ SDK `client.query` async at `:854,1122`) | `asyncio.wait_for(..., timeout)` / `TimeoutExpired` | exception |
| `skillopt/model/copilot_backend.py:128` | `copilot` CLI, env from `build_copilot_subprocess_env` (strips `COPILOT_ALLOW_ALL`) | `COPILOT_CHAT_TIMEOUT` | exception |
| `skillopt/envs/spreadsheetbench/{react_agent.py:287,executor.py:113}` | Python sandbox subprocess executing model-written code | `TimeoutExpired` handled | result dict |
| `skillopt_sleep/backend.py:658,780,847,1118,1466,1613,1758,1900,2070` | pi / claude / opencode / codex / copilot / cursor CLIs | per-call timeout, `TimeoutExpired` handled | `logging` warnings/errors (`:602,744,787,856,1539,2017`) |
| `skillopt_sleep/adapters/superpowers.py:869,1061,1199,1213` | claude CLI for Superpowers scenarios; `SKILLOPT_UNSAFE=1` adds `--dangerously-skip-permissions` | `TimeoutExpired` handled | stderr warning |
| `skillopt_sleep/scheduler.py:26,34,72,81,89` | `crontab`, `schtasks` | none | stdout notes |
| `skillopt_webui/app.py:218` (`Popen`) | `scripts/train.py` training subprocess | user-stoppable | streamed to UI |
| `plugins/copilot/mcp_server.py:249`, `plugins/copilot/skillopt/mcp_server.py:89`, `plugins/devin/mcp_server.py:211,285` | `skillopt_sleep` CLI | 3600s (copilot) / TODO | MCP responses |

## Gaps
- Retry policies are per-module, not centralized; several backends lack a documented retry (see TODO cells).
- No structured/central error log; see `docs/logging.md`.
