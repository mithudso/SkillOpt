# Environment variable names

Generated from literal `os.getenv` and `os.environ` calls in maintained Python source. Values are never collected. Dynamic role-prefixed names and variables interpreted by external CLIs also exist; see [development](DEVELOPMENT.md).

| Name | Static source |
|---|---|
| `ALFWORLD_DATA` | `skillopt/envs/alfworld/rollout.py:71` |
| `ANTHROPIC_API_KEY` | `plugins/devin/judge.py:73`, `skillopt_sleep/adapters/superpowers.py:998`, `skillopt_sleep/backend.py:766`, `skillopt_sleep/backend.py:837` |
| `APPDATA` | `plugins/devin/harvest_devin.py:56`, `plugins/devin/harvest_devin.py:72`, `skillopt_sleep/backend.py:1390`, `skillopt_sleep/harvest_opencode.py:55` |
| `AZURE_OPENAI_AD_SCOPE` | `skillopt/model/azure_openai.py:34` |
| `AZURE_OPENAI_API_KEY` | `skillopt/model/azure_openai.py:29`, `skillopt_sleep/backend.py:2321` |
| `AZURE_OPENAI_API_VERSION` | `skillopt/model/azure_openai.py:28` |
| `AZURE_OPENAI_AUTH_MODE` | `skillopt/model/azure_openai.py:33`, `skillopt_sleep/backend.py:2269` |
| `AZURE_OPENAI_ENDPOINT` | `skillopt/model/azure_openai.py:24`, `skillopt_sleep/backend.py:2250` |
| `AZURE_OPENAI_MANAGED_IDENTITY_CLIENT_ID` | `skillopt/model/azure_openai.py:38` |
| `AZURE_OPENAI_OPTIMIZER_AD_SCOPE` | `skillopt/model/azure_openai.py:85` |
| `AZURE_OPENAI_OPTIMIZER_API_KEY` | `skillopt/model/azure_openai.py:65` |
| `AZURE_OPENAI_OPTIMIZER_API_VERSION` | `skillopt/model/azure_openai.py:55` |
| `AZURE_OPENAI_OPTIMIZER_AUTH_MODE` | `skillopt/model/azure_openai.py:75` |
| `AZURE_OPENAI_OPTIMIZER_ENDPOINT` | `skillopt/model/azure_openai.py:45` |
| `AZURE_OPENAI_OPTIMIZER_MANAGED_IDENTITY_CLIENT_ID` | `skillopt/model/azure_openai.py:95` |
| `AZURE_OPENAI_TARGET_AD_SCOPE` | `skillopt/model/azure_openai.py:90` |
| `AZURE_OPENAI_TARGET_API_KEY` | `skillopt/model/azure_openai.py:70` |
| `AZURE_OPENAI_TARGET_API_VERSION` | `skillopt/model/azure_openai.py:60` |
| `AZURE_OPENAI_TARGET_AUTH_MODE` | `skillopt/model/azure_openai.py:80` |
| `AZURE_OPENAI_TARGET_ENDPOINT` | `skillopt/model/azure_openai.py:50` |
| `AZURE_OPENAI_TARGET_MANAGED_IDENTITY_CLIENT_ID` | `skillopt/model/azure_openai.py:100` |
| `CLAUDE_ALLOW_ATTACHMENT_READ` | `skillopt/model/claude_backend.py:20` |
| `CLAUDE_CLI_BIN` | `skillopt/model/claude_backend.py:17` |
| `CLAUDE_CODE_EXEC_EFFORT` | `skillopt/model/backend_config.py:69` |
| `CLAUDE_CODE_EXEC_MAX_THINKING_TOKENS` | `skillopt/model/backend_config.py:135` |
| `CLAUDE_CODE_EXEC_PATH` | `skillopt/model/backend_config.py:66` |
| `CLAUDE_CODE_EXEC_PROFILE` | `skillopt/model/backend_config.py:67` |
| `CLAUDE_CODE_EXEC_USE_SDK` | `skillopt/model/backend_config.py:68` |
| `CLAUDE_PERMISSION_MODE` | `skillopt/model/claude_backend.py:18` |
| `CLAUDE_SETTING_SOURCES` | `scripts/skillopt_skill.py:31`, `skillopt/model/claude_backend.py:19` |
| `CODEX_CLI_BIN` | `skillopt/model/backend_config.py:54`, `skillopt/model/codex_backend.py:26` |
| `CODEX_EXEC_APPROVAL_POLICY` | `skillopt/model/backend_config.py:65` |
| `CODEX_EXEC_FULL_AUTO` | `skillopt/model/backend_config.py:57` |
| `CODEX_EXEC_NETWORK_ACCESS` | `skillopt/model/backend_config.py:63` |
| `CODEX_EXEC_PATH` | `skillopt/model/backend_config.py:54`, `skillopt/model/codex_backend.py:26` |
| `CODEX_EXEC_PROFILE` | `skillopt/model/backend_config.py:56`, `skillopt/model/codex_backend.py:27` |
| `CODEX_EXEC_REASONING_EFFORT` | `skillopt/model/backend_config.py:61` |
| `CODEX_EXEC_SANDBOX` | `skillopt/model/backend_config.py:55`, `skillopt/model/codex_backend.py:28` |
| `CODEX_EXEC_USE_SDK` | `skillopt/model/backend_config.py:62` |
| `CODEX_EXEC_WEB_SEARCH` | `skillopt/model/backend_config.py:64` |
| `CODEX_PATH` | `skillopt/model/backend_config.py:54` |
| `CODEX_PROFILE` | `skillopt/model/codex_backend.py:27`, `skillopt/model/codex_backend.py:296` |
| `CODEX_SANDBOX` | `skillopt/model/backend_config.py:55` |
| `CODEX_SANDBOX_MODE` | `skillopt/model/backend_config.py:55`, `skillopt/model/codex_backend.py:28` |
| `CODEX_WORKING_DIRECTORY` | `skillopt/model/codex_backend.py:38` |
| `COPILOT_AVAILABLE_TOOLS` | `skillopt_sleep/backend.py:1744`, `skillopt_sleep/backend.py:1888` |
| `COPILOT_CHAT_OPTIMIZER_MODEL` | `skillopt/model/backend_config.py:77` |
| `COPILOT_CHAT_TARGET_MODEL` | `skillopt/model/backend_config.py:78` |
| `COPILOT_CHAT_TIMEOUT` | `skillopt/model/backend_config.py:79` |
| `COPILOT_EXEC_ALLOW_ALL_TOOLS` | `skillopt/model/backend_config.py:75` |
| `COPILOT_EXEC_HOME` | `skillopt/model/backend_config.py:73` |
| `COPILOT_EXEC_PATH` | `skillopt/model/backend_config.py:72` |
| `CURSOR_EXEC_PATH` | `skillopt/model/backend_config.py:70` |
| `CURSOR_EXEC_SANDBOX` | `skillopt/model/backend_config.py:71` |
| `DEEPSEEK_API_KEY` | `plugins/openclaw/skillopt_sleep_openclaw.py:28` |
| `DEEPSEEK_BASE_URL` | `plugins/openclaw/skillopt_sleep_openclaw.py:39` |
| `EXEC_EMPTY_RESPONSE_RETRIES` | `skillopt/model/backend_config.py:132` |
| `HOME` | `tests/test_run_sleep_fallback.py:120` |
| `LANG` | `skillopt_sleep/adapters/superpowers.py:1028` |
| `LOCALAPPDATA` | `plugins/devin/harvest_devin.py:72`, `skillopt_sleep/harvest_opencode.py:55` |
| `MINIMAX_API_KEY` | `skillopt/model/minimax_backend.py:52` |
| `MINIMAX_BASE_URL` | `skillopt/model/minimax_backend.py:50`, `skillopt/model/minimax_backend.py:51` |
| `MINIMAX_ENABLE_THINKING` | `skillopt/model/minimax_backend.py:59` |
| `MINIMAX_MAX_TOKENS` | `skillopt/model/minimax_backend.py:54` |
| `MINIMAX_REGION` | `skillopt/model/minimax_backend.py:46` |
| `MINIMAX_TEMPERATURE` | `skillopt/model/minimax_backend.py:56` |
| `MINIMAX_TIMEOUT_SECONDS` | `skillopt/model/minimax_backend.py:53` |
| `NVM_HOME` | `skillopt_sleep/backend.py:1396` |
| `OFFICEQA_DOCS_DIR` | `skillopt/envs/officeqa/tool_runtime.py:55` |
| `OFFICEQA_SEARCH_API_URL` | `skillopt/envs/officeqa/adapter.py:31` |
| `OPENAI_COMPATIBLE_MODEL` | `skillopt/model/openai_compatible_backend.py:88` |
| `OPENCODE_CONFIG` | `tests/test_backend_opencode_live.py:79` |
| `OPENCODE_CONFIG_DIR` | `tests/test_backend_opencode_live.py:85` |
| `OPENCODE_DB` | `skillopt_sleep/harvest_opencode.py:75` |
| `OPTIMIZER_AZURE_OPENAI_AD_SCOPE` | `skillopt/model/azure_openai.py:84` |
| `OPTIMIZER_AZURE_OPENAI_API_KEY` | `skillopt/model/azure_openai.py:64` |
| `OPTIMIZER_AZURE_OPENAI_API_VERSION` | `skillopt/model/azure_openai.py:54` |
| `OPTIMIZER_AZURE_OPENAI_AUTH_MODE` | `skillopt/model/azure_openai.py:74` |
| `OPTIMIZER_AZURE_OPENAI_ENDPOINT` | `skillopt/model/azure_openai.py:44` |
| `OPTIMIZER_AZURE_OPENAI_MANAGED_IDENTITY_CLIENT_ID` | `skillopt/model/azure_openai.py:94` |
| `OPTIMIZER_BACKEND` | `skillopt/model/backend_config.py:51` |
| `OPTIMIZER_DEPLOYMENT` | `skillopt/model/azure_openai.py:104`, `skillopt/model/claude_backend.py:22`, `skillopt/model/claude_code_backend.py:20`, `skillopt/model/codex_backend.py:30`, `skillopt/model/minimax_backend.py:70`, `tests/test_minimax_backend.py:199` |
| `PATH` | `skillopt/envs/spreadsheetbench/executor.py:66`, `skillopt_sleep/adapters/superpowers.py:1021` |
| `QWEN_CHAT_MODEL` | `skillopt/model/qwen_backend.py:163` |
| `REFLACT_CLAUDE_TRACE_TO_OPTIMIZER` | `skillopt/gradient/reflect.py:217` |
| `REFLACT_CODEX_TRACE_TO_OPTIMIZER` | `skillopt/gradient/reflect.py:192` |
| `REFLACT_MODEL_BACKEND` | `skillopt/model/router.py:12` |
| `SKILLOPT_CLAUDE_BIN` | `skillopt_sleep/adapters/superpowers.py:1040` |
| `SKILLOPT_DEVIN_CLAUDE_HOME` | `plugins/devin/mcp_server.py:37` |
| `SKILLOPT_DEVIN_WORKSPACES` | `plugins/devin/harvest_devin.py:128` |
| `SKILLOPT_HOST_AUTH` | `skillopt_sleep/adapters/superpowers.py:997` |
| `SKILLOPT_INHERIT_PATH` | `skillopt_sleep/adapters/superpowers.py:1020` |
| `SKILLOPT_JUDGE` | `plugins/devin/judge.py:108` |
| `SKILLOPT_JUDGE_MODEL` | `plugins/devin/judge.py:38` |
| `SKILLOPT_PROJECT_DIR` | `docs/sleep/examples/runner.py:29` |
| `SKILLOPT_PROVIDER_ENDPOINT` | `docs/sleep/examples/runner.py:26` |
| `SKILLOPT_PROVIDER_ENV_FILE` | `docs/sleep/examples/runner.py:24` |
| `SKILLOPT_PROVIDER_MODEL` | `docs/sleep/examples/runner.py:27` |
| `SKILLOPT_REPO` | `plugins/copilot/skillopt/mcp_server.py:32` |
| `SKILLOPT_ROLLOUT_LOG` | `docs/sleep/examples/runner.py:31` |
| `SKILLOPT_RUNNER` | `docs/sleep/examples/watchdog.py:17` |
| `SKILLOPT_RUN_TIMEOUT` | `plugins/copilot/skillopt/mcp_server.py:38` |
| `SKILLOPT_SLEEP_AGENT_MARKERS` | `skillopt_sleep/harvest.py:193` |
| `SKILLOPT_SLEEP_CHAT_EXTRA_BODY` | `skillopt_sleep/backend.py:2285` |
| `SKILLOPT_SLEEP_CLAUDE_MODEL` | `skillopt_sleep/backend.py:709` |
| `SKILLOPT_SLEEP_CODEX_MODEL` | `skillopt_sleep/backend.py:1436` |
| `SKILLOPT_SLEEP_CODEX_PATH` | `skillopt_sleep/backend.py:1376` |
| `SKILLOPT_SLEEP_COMPAT_MAX_TOKENS` | `skillopt_sleep/backend.py:2273` |
| `SKILLOPT_SLEEP_COPILOT_FULL_ENV` | `skillopt_sleep/backend.py:1718`, `tests/test_sleep_engine.py:2145` |
| `SKILLOPT_SLEEP_COPILOT_HOME` | `skillopt_sleep/backend.py:1723`, `tests/test_sleep_engine.py:2161` |
| `SKILLOPT_SLEEP_COPILOT_MODEL` | `skillopt_sleep/backend.py:1715` |
| `SKILLOPT_SLEEP_COPILOT_PATH` | `skillopt_sleep/backend.py:1658` |
| `SKILLOPT_SLEEP_CURSOR_MODEL` | `skillopt_sleep/backend.py:1968` |
| `SKILLOPT_SLEEP_CURSOR_PATH` | `skillopt_sleep/backend.py:1670` |
| `SKILLOPT_SLEEP_HANDOFF_DIR` | `skillopt_sleep/__main__.py:330`, `skillopt_sleep/backend.py:2544` |
| `SKILLOPT_SLEEP_OPENCODE_MODEL` | `skillopt_sleep/backend.py:1087`, `tests/test_backend_opencode_live.py:44` |
| `SKILLOPT_SLEEP_OPENCODE_PATH` | `skillopt_sleep/backend.py:907` |
| `SKILLOPT_SLEEP_PI_MODEL` | `skillopt_sleep/backend.py:578` |
| `SKILLOPT_SLEEP_PROMPTS_PATH` | `skillopt_sleep/prompts.py:165` |
| `SKILLOPT_SLEEP_REPO` | `plugins/copilot/mcp_server.py:26`, `plugins/devin/mcp_server.py:32`, `plugins/dsh/scripts/sleep.py:37` |
| `SKILLOPT_SLEEP_WORKERS` | `skillopt_sleep/consolidate.py:322`, `skillopt_sleep/replay.py:114`, `skillopt_sleep/rollout.py:76` |
| `SKILLOPT_TEST_OPENCODE_DB` | `tests/test_harvest_opencode_live.py:31` |
| `SKILLOPT_TEST_REAL_OPENCODE` | `tests/test_backend_opencode_live.py:33` |
| `SKILLOPT_TEST_REAL_OPENCODE_SOURCE` | `tests/test_harvest_opencode_live.py:22` |
| `SKILLOPT_UNSAFE` | `skillopt_sleep/adapters/superpowers.py:1048` |
| `SKILLOPT_WATCHDOG_INTERVAL` | `docs/sleep/examples/watchdog.py:16` |
| `SKILLOPT_WATCHDOG_LOG` | `docs/sleep/examples/watchdog.py:18` |
| `SYSTEMROOT` | `skillopt/envs/spreadsheetbench/executor.py:76` |
| `SystemRoot` | `skillopt/envs/spreadsheetbench/executor.py:77` |
| `TARGET_AZURE_OPENAI_AD_SCOPE` | `skillopt/model/azure_openai.py:89` |
| `TARGET_AZURE_OPENAI_API_KEY` | `skillopt/model/azure_openai.py:69` |
| `TARGET_AZURE_OPENAI_API_VERSION` | `skillopt/model/azure_openai.py:59` |
| `TARGET_AZURE_OPENAI_AUTH_MODE` | `skillopt/model/azure_openai.py:79` |
| `TARGET_AZURE_OPENAI_ENDPOINT` | `skillopt/model/azure_openai.py:49` |
| `TARGET_AZURE_OPENAI_MANAGED_IDENTITY_CLIENT_ID` | `skillopt/model/azure_openai.py:99` |
| `TARGET_BACKEND` | `skillopt/model/backend_config.py:52` |
| `TARGET_DEPLOYMENT` | `skillopt/model/azure_openai.py:105`, `skillopt/model/claude_backend.py:23`, `skillopt/model/claude_code_backend.py:21`, `skillopt/model/codex_backend.py:31`, `skillopt/model/minimax_backend.py:66`, `tests/test_minimax_backend.py:195` |
| `TERM` | `skillopt_sleep/adapters/superpowers.py:1027` |
| `TZ` | `tests/test_copilot_harvest.py:225` |
| `USERPROFILE` | `skillopt_sleep/backend.py:1393` |
| `WINDIR` | `skillopt/envs/spreadsheetbench/executor.py:78` |
| `XDG_CONFIG_HOME` | `plugins/devin/harvest_devin.py:61` |
| `XDG_DATA_HOME` | `skillopt_sleep/harvest_opencode.py:49` |
