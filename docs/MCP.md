# MCP adapters

SkillOpt supplies small stdio JSON-RPC adapters. They run on demand under an MCP
client; the repository does not require a persistent MCP service for development.
No adapter was activated by the maintenance workflow.

| Adapter | Launch from the repository root | Tools |
|---|---|---|
| Copilot Sleep | `python plugins/copilot/mcp_server.py` | `sleep_status`, `sleep_dry_run`, `sleep_run`, `sleep_adopt`, `sleep_harvest`, `sleep_schedule`, `sleep_unschedule` |
| Devin Sleep | `python plugins/devin/mcp_server.py` | The same seven `sleep_*` tools; data-reading actions first convert local Devin history. |
| Research wrapper | `python plugins/copilot/skillopt/mcp_server.py` | `skillopt_list_configs`, `skillopt_train`, `skillopt_eval` |

The Sleep adapters declare protocol version `2024-11-05`. Their `TOOLS` declarations
and runtime argument checks are the source of truth. The research wrapper is a
separate adapter, with three tools. Do not count it as another seven-tool Sleep
server. The generated [tool inventory](tool-inventory.json) records each adapter
separately.

## Configuration and authority

Use the adapter's `mcp-config.example.json` and its README. Set
`SKILLOPT_SLEEP_REPO` when the installation cannot discover the checkout. Devin
also supports `SKILLOPT_DEVIN_WORKSPACES` and `SKILLOPT_DEVIN_CLAUDE_HOME`; these
point at local history and converted output. Keep machine-specific client
configuration and credentials outside version control.

The default mock backend does not require provider credentials. Real backends use
their configured environment or CLI login. `sleep_run` stages proposals;
`sleep_adopt` changes live documents, and scheduling tools change the user's
scheduler. A dry run may still read history and invoke a configured real model.
Choose a disposable project, reviewed task file and mock backend for a synthetic
exercise. Do not invoke a history-reading tool as a health check on a real profile.

## Validation and extension

`tests/test_mcp_schema.py` and `tests/test_devin_plugin.py` exercise tools and
subprocess results with fixtures. `tests/test_plugin_sync.py` protects standalone
plugin copies. Add argument validation and synthetic tests when adding a tool;
keep the declared tools, generated inventory and user documentation synchronized.
Use the repository's stdlib/Python tooling rather than adding a Node server to
support these adapters.
