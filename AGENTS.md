# Backend Base Agent Guide

This file defines the long-term collaboration rules for agents working in `black-tonny-backend-base`.

If direct task instructions or source-of-truth repository docs differ, follow them first.

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
- Do not commit, push, or create a PR until the user has clearly said the change is approved for submission.
- If the current branch or worktree is dirty, prefer a clean branch or clean worktree for final PR preparation.

## Output Defaults

- Do not keep repeating repository background once it is established.
- Do not reprint full PR descriptions unless the user explicitly asks for them.
- If local scripts can generate a diff, changed-file list, PR draft, or migration anchors, prefer using those outputs instead of hand-rebuilding them.
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
