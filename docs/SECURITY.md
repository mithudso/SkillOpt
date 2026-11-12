# Security model

SkillOpt runs developer tools and model-driven experiments with the permissions of
the invoking user. SkillOpt-Sleep reads local agent history and proposes document
edits. Treat task files, model output, imported transcripts and staged artifacts as
sensitive input. These tools provide integrity checks; they are not an operating
system sandbox for hostile code or another process running as the same user.

## Principals and trust boundaries

| Boundary | Data and authority | Controls and limits |
|---|---|---|
| Operator to CLI | Configuration, paths, backend and adoption choices | Review arguments and output paths; use a disposable project for tests. |
| Local history to Sleep | Agent transcripts can contain credentials and private text | Limit source homes and project scope; review mined tasks before external use. |
| Model to research runner | Text, tool calls and generated code | Backend policy controls tools; SpreadsheetBench executes generated Python in a subprocess. A timeout is not a security sandbox. |
| Proposal to live document | `SKILL.md` and `CLAUDE.md` edits | Explicit adoption, baseline hashes, canonical paths, backups, receipts and a recovery journal. See [adoption](sleep/multi-skill-staging.md). |
| Backend to provider | Prompts, attachments, tokens and credentials | Endpoint/auth configuration, timeouts and failure handling depend on the backend. Use approved endpoints and synthetic data for tests. |
| Browser to WebUI | Configuration and training controls | Bind locally by default. `--share` or a nonlocal host requires a separate access-control decision. The UI can launch training as the user. |
| MCP client to adapter | Tool names and typed arguments | Adapter validation and subprocess argument lists. Adoption and scheduling remain state-changing operations. |

## Threat review

| STRIDE area | Review focus |
|---|---|
| Spoofing | Verify the selected backend executable and provider endpoint. Do not send Azure credentials to an arbitrary compatible URL. |
| Tampering | Check staging hashes, file identities, containment and recovery evidence before changing live documents. Do not bypass a stale adoption lock. |
| Repudiation | Preserve run reports and adoption receipts. Application logs are operational evidence, not an authenticated audit service. |
| Information disclosure | Redact credentials from diagnostics and reports. Keep transcripts, datasets, `.env`, outputs and authentication stores out of commits. |
| Denial of service | Bound worker counts, requests, subprocess duration and input sizes. Treat model and CLI retries as potentially costly. |
| Elevation of privilege | Keep model tools disabled on text-only paths. Use an external sandbox for executable tasks; a temporary working directory does not constrain filesystem access. |

## Authentication and secret handling

Provider credentials belong in the environment or the provider CLI's own credential
store. The repository's `.env.example` contains names and placeholders. Do not
commit `.env`, `.mcp.json`, `.skillopt-sleep/`, `outputs/`, real task sets or exported
sessions. Never include credential values in exceptions, reports or test fixtures.
Rotate a disclosed credential through its provider and remove it from new output;
deleting one file does not revoke a credential or remove Git history.

The research trainer redacts configuration before persisting it. Sleep uses
`skillopt_sleep.staging.redact_secrets` for credential-shaped text and mappings.
Pattern redaction cannot prove that arbitrary prose contains no private data.

## Verification and reporting

Use mocks and scratch HOME/data/auth/model locations for maintenance verification.
Block outbound connections for the entire test process tree. Do not use live
provider inference, real browser profiles, customer sessions or existing model
caches to verify a source change. See [testing](TESTING.md) and the
[maintenance runbook](runbooks/maintenance.md).

Report upstream vulnerabilities using the root [security policy](https://github.com/mithudso/SkillOpt/blob/main/SECURITY.md).
For a fork-only issue, use private reporting in the personal repository's Security
tab when available. Do not place sensitive reproductions in a public issue. This
fork does not add a response-time commitment or a compliance certification.
