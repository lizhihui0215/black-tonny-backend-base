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
- [`transform-input-boundary.md`](./transform-input-boundary.md)
  - Minimal future transform input boundary derived from the current formal capture boundary
  - Language: English
  - Status: `Source of truth`
- [`admitted-transform-input-boundary.md`](./admitted-transform-input-boundary.md)
  - Minimal future admitted transform input boundary derived from the broader transform input candidate layer
  - Language: English
  - Status: `Source of truth`
- [`transform-readiness-boundary.md`](./transform-readiness-boundary.md)
  - Minimal future transform readiness boundary derived from the narrower admitted transform input layer
  - Language: English
  - Status: `Source of truth`

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
