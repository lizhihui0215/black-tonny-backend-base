# Backend Base Agent Guide

This file defines the long-term collaboration rules for any coding agent working in `black-tonny-backend-base`.

If direct task instructions or source-of-truth repository docs differ, follow them first.
If context is incomplete, read this file and the directly related repository files before making repository-fact judgments or change recommendations.

## Repository Facts

- `black-tonny-backend-base` uses PostgreSQL, not MySQL.
- The current migration mainline is `capture` + docs + research support.
- `capture` is the formal landing layer, not a research evidence warehouse.
- research support needs to migrate in, but it is not the runtime source of truth.
- docs migrate in stages and should be treated as a long-running track, not one-shot cleanup.

## Boundary Rules

- Do not mechanically copy the legacy flat `app/services` structure into the base repo.
- Do not treat compat shims as formal implementations.
- Do not make `transform` or `serving` the default migration target unless the task explicitly asks for them.
- Keep every PR scoped to one goal.

## Workflow

- Default three-role collaboration mode for source-intelligence work:
  - `ChatGPT` is the review authority. It reviews against the current plan, gate, and truth discipline; it should not silently expand scope.
  - `User` is relay-only by default. Keep user work to copy/paste handoff unless real git/worktree truth must be fetched.
  - `Codex` is the executor. It implements the current allowed scope, prepares the review packet, absorbs review feedback, and handles submission after approval.
- Use the default sequence: implement -> review -> submit.
- Default source-intelligence sequence: `Codex implement -> Codex produce review packet -> User forward to ChatGPT -> ChatGPT review -> User paste review back -> Codex revise or submit`.
- Keep follow-up work for an existing PR inside that PR's current goal unless the user explicitly approves a scope change or asks for a new PR.
- For source-intelligence migration work, treat `docs/source-intelligence/ops/full-migration-master-plan.md` as the collaboration control plane for current milestone / PR / status / next allowed step.
- For each completed round of repository changes, also sync the current execution state in `docs/source-intelligence/ops/full-migration-master-plan.md`. Update the relevant milestone / PR / status snapshot so the plan remains traceable and ready for GPT review with the latest movement.
- A source-intelligence round is not complete until the master plan current-execution snapshot and latest standard status sync block are updated.
- Effective rounds include file-change rounds, review-verdict change rounds, next-allowed-step change rounds, and state-correction-only rounds. `changed files: none` is still valid when the round changes state.
- Do not commit, push, or create a PR until the user has clearly said the change is approved for submission.
- If the current branch or worktree is dirty, prefer a clean branch or clean worktree for final PR preparation.

## Output Defaults

- Do not keep repeating repository background once it is established.
- Do not reprint full PR descriptions unless the user explicitly asks for them.
- Treat diffs, changed-file lists, PR drafts, and migration anchors as mechanical outputs; use repo-local scripts to generate them whenever practical instead of hand-rebuilding them.
- For review handoff, default to direct-forward first: produce a compact review packet the user can paste to ChatGPT without reorganizing it. Only fall back to command-first handoff when real-time git/worktree truth is required and cannot be safely summarized.
- Default to the smallest useful output set: plan, validation summary, diff, and minimal PR template draft.
- For source-intelligence rounds, the default output set must also include:
  - round conclusion
  - current milestone / PR / status
  - changed files
  - validation
  - risks
  - next allowed step
  - a ready-to-forward ChatGPT review packet
  - the latest completed status sync block
- For source-intelligence rounds, Codex must generate the latest completed status sync block directly; the user should not have to compose or normalize it manually.
- If the latest status sync block is missing, treat the round as not closed.

## Local Scripts

- `scripts/copy-pr-diff`
- `scripts/copy-changed-files`
- `scripts/copy-pr-template-draft`
- `scripts/copy-migration-anchors`

## PR Template Alignment

Agent-written PR summaries should align to the current repository template:

- `PR Goal`
- `Changed Files`
- `Boundary Check`
- `Not Migrated`
- `Risks`
- `Validation`
