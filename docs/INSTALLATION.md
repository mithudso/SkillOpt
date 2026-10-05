# Installation

Authoritative guide: `docs/guide/installation.md`. Summary (verified against `pyproject.toml`):

- Python >=3.10. Core deps: openai, pyyaml, numpy, openpyxl, azure-identity, azure-core, httpx.
- From source (this fork): `git clone https://github.com/mithudso/SkillOpt.git && cd SkillOpt && pip install -e ".[dev]"`.
- Extras: `alfworld`, `claude`, `qwen`, `searchqa`, `docs`, `webui`, `dev`, `all` (alfworld+claude deps only).
- Console scripts: `skillopt-train`, `skillopt-eval`, `skillopt-sleep`.
- Credentials: copy `.env.example` to `.env`, fill in, `set -a; source .env; set +a`. The `mock` Sleep backend needs none.
- Verify: `python -m pytest -q`; `skillopt-sleep run --backend mock --help`.
- Upgrade: `git fetch upstream && git merge upstream/main && pip install -e ".[dev]"`. Uninstall: `pip uninstall skillopt`.
- Agent plugins: see `plugins/README.md` and each `plugins/<name>/README.md`.
