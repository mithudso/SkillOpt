# Requirements

## Functional behavior

1. The research CLI loads layered YAML configuration and runs an environment
   adapter through rollout, reflection, aggregation, selection, update and gating.
2. Optimizer and target roles may select different model backends. Optional
   environments remain lazy so installing the core package does not install
   benchmark engines or local model runtimes.
3. The fork's `scripts/skillopt_skill.py` registers the `skilltask` environment for
   training or evaluating an arbitrary skill against an operator-supplied task set.
4. Sleep harvests configured sources, mines recurring tasks, replays tasks,
   evaluates proposals and stages reviewed edits. Adoption is explicit unless the
   operator selects automatic adoption.
5. Standalone agent integrations wrap the shared Sleep engine. They must preserve
   the CLI's validation, error status and adoption boundaries.
6. The optional Gradio UI configures and supervises a training subprocess. The UI
   is not required for CLI or Sleep use.

## Compatibility and dependencies

Python **3.10 or newer** is declared in `pyproject.toml`; CI exercises Python
3.10, 3.11 and 3.12. The authoritative core dependencies are `openai`, `pyyaml`,
`numpy`, `openpyxl`, `azure-identity`, `azure-core` and `httpx`. Read their version
bounds in [pyproject.toml](https://github.com/mithudso/SkillOpt/blob/main/pyproject.toml); these are ranges, not a reproducible
lock. Use a project virtual environment and record the resolved environment for a
reproduction.

Extras cover ALFWorld, Claude, Qwen, SearchQA data materialization, documentation,
WebUI and development tools. The `all` extra does not include every other extra.
Heavy optional runtimes and datasets require an explicit installation decision;
ordinary tests do not require model weights, a GPU or live provider access.

The dsh plugin has its own npm manifest and Cordis/Schemastery integration. Other
plugins use Python, shell or PowerShell. Linux, macOS and Windows paths exist in
the source; platform-specific scheduling and shell behavior require appropriate
platform checks. No hardware performance minimum or latency SLA is enforced.

## Quality and operational constraints

- Changed behavior needs assertions for success, failure and relevant boundary
  inputs. [Testing](TESTING.md) records the gates actually enforced.
- Preserve held-out split identities. Synthetic unit-test results do not measure
  model quality, optimization gain or real provider fidelity.
- Bound subprocesses and provider requests, preserve actionable diagnostics and
  avoid caching transient failures as successful answers.
- Keep secrets, sessions, datasets, outputs and semantic stores outside generated
  documentation. Static metadata indexes must have valid repository-relative paths.
- Service activation, scheduler installation, live adoption, inference, downloads
  of model weights and embedding operations require their own explicit scope.
