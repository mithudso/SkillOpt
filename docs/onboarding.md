# Onboarding

1. Read `CLAUDE.md` (layout, commands, fork rules), then `docs/ARCHITECTURE.md`.
2. Install: `pip install -e ".[dev]"` and run `python -m pytest -q`.
3. Try Sleep with no credentials: `skillopt-sleep run --backend mock` (see `docs/sleep/README.md`).
4. Understand the loop: `docs/guide/training-loop.md`, `docs/guide/dl-analogy.md`, `docs/guide/skill-document.md`.
5. First research run: `docs/guide/first-experiment.md` (SearchQA config `configs/searchqa/default.yaml`); local smoke: `docs/guide/local-env-smoke.md`.
6. Configure backends: `docs/guide/configuration.md`, `.env.example`, `docs/DEVELOPMENT.md`.
7. Extend: `docs/guide/new-benchmark.md`, `docs/guide/new-backend.md`, `skillopt/envs/_template/`.
8. Agent integrations: `plugins/README.md`, `AGENTS.md`.
9. Fork workflow: additive files only; sync via `git fetch upstream && git merge upstream/main`; log work in `memory.md` and `prompts.md`.
10. Upstream contribution rules: `CONTRIBUTING.md`, `docs/review_guidelines.md`.
