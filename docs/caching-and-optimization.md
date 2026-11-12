# Caching and performance

## Existing layers

| Layer | Lifetime and invalidation | Constraints |
|---|---|---|
| Sleep CLI response cache (`skillopt_sleep/backend.py`) | One backend instance; keys include operation and prompt/skill hashes | Preserve repeated-rollout sample identity. Failed calls must remain retryable. This is not a durable provider cache. |
| Research rollout reuse (`skillopt/engine/trainer.py`) | Trainer/run state | Reuse must respect skill, split and configuration identity. Never merge held-out data into training. |
| Azure clients and token providers (`skillopt/model/azure_openai.py`) | Process-level clients and provider-managed token lifetime | Runtime configuration changes must reset the appropriate clients. Do not log credentials or token contents. |
| Python imports and lazy environment registration | Interpreter lifetime | Optional backend and benchmark dependencies should load only when selected. |
| Local run artifacts | Operator-selected output directory | These are experiment records, not a universal cache; preserve them unless cleanup is explicitly authorized. |

The repository has no Redis, CDN or database query cache to administer. It does not
require a background semantic indexer. Generated documentation indexes are static
metadata and do not contain vectors or model outputs.

## Reviewing performance changes

Check correctness and resource ownership before adding caching or concurrency.
Backend state, environment variables and import patches are shared within a
process, so blanket parallel test execution needs evidence of isolation. Keep
different task/sample identities separate even when their text matches.

Use a synthetic callable and deterministic synchronization to test cache misses,
failure recovery and concurrent requests. Avoid timing sleeps as race detectors.
Profile an explicitly authorized workload with `python -m cProfile`; do not use
private transcripts, frozen benchmarks or a live provider merely to measure a
maintenance change. Report a measured performance claim only with its workload,
environment and limitations. The maintenance test count is not a quality score.
