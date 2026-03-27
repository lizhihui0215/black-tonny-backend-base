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

- Use the default sequence: implement -> review -> submit.
- Keep follow-up work for an existing PR inside that PR's current goal unless the user explicitly approves a scope change or asks for a new PR.
- Do not commit, push, or create a PR until the user has clearly said the change is approved for submission.
- If the current branch or worktree is dirty, prefer a clean branch or clean worktree for final PR preparation.

## Output Defaults

- Do not keep repeating repository background once it is established.
- Do not reprint full PR descriptions unless the user explicitly asks for them.
- Treat diffs, changed-file lists, PR drafts, and migration anchors as mechanical outputs; use repo-local scripts to generate them whenever practical instead of hand-rebuilding them.
- For review handoff, do not default to inline diffs or raw logs. Prefer command-first output: give the user a small executable command, let them run it, and review the returned result. On macOS, prefer `pbcopy` when practical. Only inline large raw output when the user explicitly requests it.
- Default to the smallest useful output set: plan, validation summary, diff, and minimal PR template draft.

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
