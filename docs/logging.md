# Logging

How the code actually logs (grep of `print(`, `logging`, `getLogger`, 2026-10-05):

- **Research loop (`skillopt/`, `scripts/`)**: `print` to stdout for progress (heaviest in `skillopt/engine/trainer.py`, `scripts/train.py`). No `logging` config. Persistent records are files under `out_root`: step directories, `history.json`-style records, `lr_history.jsonl`, `appendix_notes.json` (written by `trainer.py`), saved skills per step. `_redact_cfg` in `trainer.py` redacts config values before saving.
- **Console encoding**: `skillopt/utils/console.py:force_utf8_stdout_stderr` avoids `UnicodeEncodeError` on Windows.
- **Sleep (`skillopt_sleep/`)**: CLI output via `print` (`__main__.py`, `--json` for machine output, `--progress`); `logging.getLogger("skillopt_sleep")` warnings/errors in `backend.py` (CLI failures, timeouts); per-night `evidence.jsonl` chain (`evidence.py`, toggle `evidence_log`); cron output to `<project>/.skillopt-sleep/cron.log` (`scheduler.py`). No `basicConfig`, so library warnings only show via Python's last-resort handler (WARNING+ to stderr).
- **WebUI**: training subprocess stdout/stderr merged and streamed into the UI (`skillopt_webui/app.py`).
- **Sensitive data**: `skillopt_sleep/staging.py:redact_secrets` scrubs secrets from staged artifacts; trainer redacts config. Do not log API keys or transcript contents.

## Gaps (TODO)
- No structured logging, levels, or correlation ids in the research loop.
- External-call failures are mostly surfaced as exceptions, not logged with request/outcome (see `docs/external-calls.md`).
- No tests assert log output (TODO: add via `caplog` for `skillopt_sleep` warnings).
