# Components

| Component | Path | Purpose | Key API / entry | Depends on |
|---|---|---|---|---|
| Trainer | `skillopt/engine/trainer.py` | runs the epoch/step loop, gate, state persistence | `ReflACTTrainer(cfg, adapter).train()` | gradient, optimizer, evaluation, model |
| Config | `skillopt/config.py` | load/merge YAML config | see `docs/reference/config.md` | pyyaml |
| Types / utils | `skillopt/types.py`, `skillopt/utils/{scoring,json_utils,console}.py` | shared dataclasses, scoring, tolerant JSON extraction (`json_repair` optional), UTF-8 console | `compute_score`, `skill_hash`, `force_utf8_stdout_stderr` | - |
| Datasets | `skillopt/datasets/base.py` | `BatchSpec`, dataloader base | | |
| Gradient | `skillopt/gradient/{reflect,aggregate}.py` | analyst edits + hierarchical merge | `merge_patches` | model, prompts |
| Optimizer | `skillopt/optimizer/*.py` | clip/select, LR schedulers, patch apply, rewrite, appendix, slow update, meta skill | `rank_and_select`, `apply_patch_with_report`, `build_scheduler` | model |
| Gate | `skillopt/evaluation/gate.py` | accept/reject decision | `evaluate_gate`, `select_gate_score` | - |
| Model backends | `skillopt/model/*.py` | LLM call adapters + router | `router.set_backend`, `call_llm` style functions per module | openai, azure-identity, CLIs |
| Envs | `skillopt/envs/<name>/` | adapters: dataloader, rollout, evaluator, reflect, prompts, seed skills | `EnvAdapter` (`envs/base.py`) | datasets, model |
| Prompts | `skillopt/prompts/*.md` | analyst/merge/rank/rewrite/slow-update/meta prompts | | |
| Sleep cycle | `skillopt_sleep/cycle.py` | nightly orchestrator | `run_sleep_cycle` | all sleep modules |
| Sleep harvest | `skillopt_sleep/harvest*.py` | transcript readers per agent | `harvest_for_config` | local files/SQLite |
| Sleep mine/replay | `mine.py`, `llm_miner.py`, `replay.py`, `rollout.py`, `judges.py` | task mining, replay, scoring | | backend |
| Sleep consolidate | `consolidate.py`, `dream.py`, `slow_update.py`, `multi_skill.py`, `gate.py` | edit proposals + gate, multi-skill fan-out | `consolidate`, `evaluate_gate` | backend |
| Sleep staging | `staging.py`, `skill_resolver.py`, `memory.py` | proposals, adopt transaction, skill path resolution | `write_staging`, `adopt` | filesystem |
| Sleep backends | `skillopt_sleep/backend.py`, `handoff_backend.py` | model/CLI backends | `get_backend`, `build_backend` | CLIs, openai |
| Sleep evalkit | `evalkit.py` | paired A/B stats | `skillopt-sleep evalkit` | |
| Sleep scheduler | `scheduler.py` | cron/schtasks install | `schedule`/`unschedule` | crontab, schtasks |
| Sleep adapters | `adapters/superpowers.py` | Superpowers skill replay adapter | | claude CLI |
| Sleep experiments | `experiments/*.py` | persona/gbrain/transfer/sweep experiment runners | | |
| WebUI | `skillopt_webui/app.py` | Gradio dashboard | `python -m skillopt_webui` | gradio (extra) |
| CLIs | `scripts/train.py`, `scripts/eval_only.py`, `scripts/materialize_searchqa.py`, `scripts/run_*.sh`, `scripts/smoke_superpowers.sh` | entry points and benchmark launchers | `skillopt-train`, `skillopt-eval` | |
| Plugins | `plugins/*` | agent integrations | see `AGENTS.md` | skillopt_sleep |
