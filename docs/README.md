# Backend Base Docs Index

This directory contains topic-level documentation for `black-tonny-backend-base`.

## How To Use This Index

Start from the repository [README](../README.md), then use the sections below based on the kind of document you need:
- formal docs for current repository truth
- migration planning docs for scoped planning work
- reference docs for legacy inputs that are intentionally non-runtime
- archive docs for superseded legacy context

Only the formal docs define current repository behavior.
That includes the current capture formal boundary under `src/app/**` and `src/migrations/**`.
`docs/reference/**` and `src/examples/**` are reference-only areas for research, traceability, samples, troubleshooting, and transition patterns.

## Language Note

Top-level public entry docs remain in English:
- [`../README.md`](../README.md)

Formal docs in this directory are maintained in English.
Internal planning, reference, and archive material can stay in Chinese when it is migration-supporting content.

## Formal Docs

- [`runtime-boundaries.md`](./runtime-boundaries.md)
  - Current runtime structure, route groups, package boundaries, and migration guardrails
  - Language: English
  - Status: `Source of truth`
- [`capture-serving-boundary.md`](./capture-serving-boundary.md)
  - Current dual-database responsibilities and the serving-only runtime read rule
  - Language: English
  - Status: `Source of truth`
- [`capture-minimal-boundary.md`](./capture-minimal-boundary.md)
  - Minimal formal capture boundary across models, schemas, CRUD helpers, and migration targets
  - Language: English
  - Status: `Source of truth`
- [`serving-projection-minimal-boundary.md`](./serving-projection-minimal-boundary.md)
  - Minimal formal serving projection boundary across models, schemas, CRUD helpers, and migration targets
  - Language: English
  - Status: `Source of truth`
- [`transform-input-boundary.md`](./transform-input-boundary.md)
  - Minimal future transform input boundary derived from the current formal capture boundary
  - Language: English
  - Status: `Source of truth`
- [`admitted-transform-input-boundary.md`](./admitted-transform-input-boundary.md)
  - Minimal admitted transform input boundary and selector derived from the broader transform input candidate layer
  - Language: English
  - Status: `Source of truth`
- [`transform-readiness-boundary.md`](./transform-readiness-boundary.md)
  - Minimal future transform readiness boundary derived from the narrower admitted transform input layer
  - Language: English
  - Status: `Source of truth`
- [`transform-state-transition-boundary.md`](./transform-state-transition-boundary.md)
  - Minimal future transform state-transition boundary derived from the narrower transform readiness layer
  - Language: English
  - Status: `Source of truth`
- [`capture-batch-field-semantics.md`](./capture-batch-field-semantics.md)
  - Current semantics and ownership boundary of transform-adjacent fields on `capture_batches`
  - Language: English
  - Status: `Source of truth`
- [`transform-rule-set-questions.md`](./transform-rule-set-questions.md)
  - Minimum future question list that a scoped transform rule-set must answer explicitly
  - Language: English
  - Status: `Source of truth`

## Current Surface Notes

- [`research-support-current-surface.md`](./research-support-current-surface.md)
  - Current research support code surface and its minimal formal contract boundary
  - Language: English
  - Status: `Current surface note`
- [`legacy-research-bridge-note.md`](./legacy-research-bridge-note.md)
  - Bridge note between legacy research reference and the current minimal surface
  - Language: English
  - Status: `Current surface note`
- [`legacy-capture-bridge-note.md`](./legacy-capture-bridge-note.md)
  - Bridge note between legacy capture reference and the current minimal capture surface
  - Language: English
  - Status: `Current surface note`

## Migration Planning

- [`legacy-backend-migration-mapping.md`](./legacy-backend-migration-mapping.md)
  - PR-1 inventory, classification, old-path to new-path mapping, capture scope list, and research/runtime boundary notes
  - Language: Chinese working doc
  - Status: `Source of truth for PR-1 migration planning`

## Reference Docs

- [`reference/legacy-backend/README.md`](./reference/legacy-backend/README.md)
  - Reserved reference-only area for selectively retained legacy research material
  - Language: Chinese working doc
  - Status: `Reference`

## Archive Docs

- [`archive/legacy-runtime/README.md`](./archive/legacy-runtime/README.md)
  - Reserved archive area for superseded legacy runtime documentation
  - Language: Chinese working doc
  - Status: `Archive`
