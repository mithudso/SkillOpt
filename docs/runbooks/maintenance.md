# Source maintenance and recovery

## Preconditions

Verify the exact personal repository identity and default branch. Inspect the
working tree, linked worktrees, effective Git hooks and active ownership. Preserve
other changes and live installations. Fetch only the authorized personal remote;
upstream synchronization is a separate operation.

Use an isolated task worktree. Inventory maintained paths and hashes, with explicit
exclusions for datasets, model prompts, checkpoints, vendored implementations and
private state. Keep raw execution logs and private findings outside the repository.

## Synthetic verification

1. Read the detected test/build commands before running them. Create a disposable
   environment with scratch HOME, data, model, auth, cache and temporary paths.
2. Disable live provider tests. Install synthetic adapters before risky imports;
   prevent local inference and cached-model loading as well as network access.
3. Run tests behind a process-tree network guard. Deny outbound and loopback
   connections. Grant only an exact port owned by a synthetic listener when that
   test needs one. Do not query a developer daemon as a connectivity check.
4. Before a Git fixture initializes, strip inherited `GIT_*` selectors and config
   overrides. Use an explicit empty template, fixture-only empty global/system
   configuration and `GIT_TERMINAL_PROMPT=0`. Verify the effective hook directory
   before its first commit. Preserve these settings through descendant commits.
5. Exercise a hostile-template/global-hook sentinel. A temporary directory alone
   does not prove that a fixture cannot inherit an indexing hook.
6. Record baseline results, add a failing synthetic counterexample for a defect,
   apply the focused repair and run relevant checks to green. Record skipped or
   unsafe checks explicitly.

## Adoption recovery

Stop competing adoption and live editing before inspecting a failed transaction.
Preserve the staging directory, journal, receipts and backups. A stale lock fails
closed; do not guess that it can be deleted. Confirm no adopting process owns it,
then inspect the source contract and seek operator review when recovery evidence
is inconsistent. Never overwrite a live file that changed after the transaction.
See the detailed [integrity contract](../sleep/multi-skill-staging.md).

## Delivery and rollback

Review the complete task-owned diff and stage explicit files. Commit, push a task
branch, open a PR against the exact personal repository, and wait for every final
check. Merge only the passing final commit. Verify the merged PR and remote default
tree/blob content; a squash merge has a different commit identity.

Fast-forward a clean, nondivergent primary checkout only when that preserves active
work. Remove only the task's clean merged worktree and branch. Keep a local receipt
with the PR URL, merge commit, checks, content proof, source coverage and limits.

For a delivered regression, prepare a revert PR and run the same relevant checks.
Do not rewrite the default branch. For uncommitted task changes, restore only the
documented task-owned originals from the run's central snapshot and remove only
the files that run created. Never apply a blanket restore to a shared checkout.
