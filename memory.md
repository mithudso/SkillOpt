# memory.md — SkillOpt fork operator log

Versioned log of work on this fork (independent of package version 0.2.0). Newest first.

## v0.3 - 2026-10-05

**Active task:** Stele knowledge graph for the fork.

**Completed**
- Created private Stele project `skillopt-ocj5r` (SkillOpt) and bound the repo via `.stele/project.json` (previously inherited the `dev-y3seh` umbrella binding from `/Users/mitch/dev/.stele`).
- Ran `/stele:backfill`: 17 extraction missions + 11 verifier batches over docs, code, 572 commits and upstream microsoft/SkillOpt issues/PRs. Inserted 15 components, 370 knowledge nodes, 24 verified tasks, 10 imported docs. Agent sessions not mined (none with 5+ turns).
- Fixed CLAUDE.md and docs/COMPONENTS.md: Sleep comparison subcommand is `evalkit`, not `eval`; listed `.stele/project.json` as fork-only.

**Next steps (tracked as Stele tasks)**
- TASK-231: `skillopt/model/claude_backend.py` passes `--schema`; Claude CLI only accepts `--json-schema`, so `claude_chat` structured output (`return_message=True`) fails.
- TASK-284: skilltask `grade()` runs outside the try in `_rollout_one`, so one judge exception aborts the batch; `env.exec_timeout` is ignored by `SkillTaskAdapter`.
- TASK-125: run `skillopt-run` on a real skill with a hard task set to measure a gain.

## v0.2 - 2026-10-05 (logged retroactively)

**Completed**
- Commit `f4232fe`: skilltask prepends `DEFAULT_ANSWER_PREAMBLE` (`skillopt/envs/skilltask/rollout.py`) to every task input. Reason: `claude_chat` runs the target inside `claude -p` with tools denied; on a 38-task run several rollouts answered "Bash and Read were denied" and reflection learned a bogus patch from that noise. Config key `env.answer_preamble` (unset = default, `""` = off).

## v0.1 - 2026-10-05

**Active task:** fork + repo bootstrap.

**Completed**
- Forked `microsoft/SkillOpt` to `github.com/mithudso/SkillOpt` (`origin`); `upstream` = `github.com/microsoft/SkillOpt`.
- Ran repo-bootstrapper `update_to_ideal_repo` additively (new files only): `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `memory.md`, `prompts.md`, `.editorconfig`, `.gitattributes`, `docs/{ARCHITECTURE,DEVELOPMENT,COMPONENTS,TESTING,INSTALLATION,known-issues,external-calls,integrations-and-assumptions,logging,onboarding,codebase-overview}.md`, `docs/high_signal_file_index.json`, `docs/repo-bootstrap-audit-2026-10-05.md`.
- Wrote usage llms family at repo root: `llms.txt` (index), `llms-small.txt` (cited how-to), `llms-facts.txt` (315+ `fact — path:line`), `llms-full.txt` (rebuild: `python scripts/build_llms_full.py`).
- Added generic `skilltask` env (`skillopt/envs/skilltask/`, `configs/skilltask/default.yaml`, launcher `scripts/skillopt_skill.py`, tests `tests/test_skilltask_env.py`) so any SKILL.md can be trained against a JSONL task set.
- Added Claude Code skill `/Users/mitch/.claude/skills/skillopt-run/` (prepare_run.py → launch.sh → finalize.py). Smoke run (12 tasks, 1 epoch, haiku) passed end to end in 83 s.

**Next steps**
- Run `skillopt-run` on a real skill with a hard task set (baseline < 1.0) to measure an actual gain.
- Triage ruff findings (143 at bootstrap time) upstream-friendly; see `docs/known-issues.md`.
- Sync with upstream periodically (`git fetch upstream && git merge upstream/main`).
