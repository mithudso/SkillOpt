# memory.md — SkillOpt fork operator log

Versioned log of work on this fork (independent of package version 0.2.0). Newest first.

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
