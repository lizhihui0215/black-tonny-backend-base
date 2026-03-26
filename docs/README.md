# Backend Base Docs Index

This directory contains topic-level documentation for `black-tonny-backend-base`.

## Current Scope

`black-tonny-backend-base` is the only source of truth for ongoing backend migration work.

The current documentation phase is intentionally narrow:
- audit legacy documentation from `black-tonny-backend`
- classify what can become formal documentation here
- keep research material reference-only
- keep superseded runtime material in archive-only planning

This phase does not migrate business code, scripts, or runtime wiring.

## Language Note

Top-level public entry docs remain in English:
- [`../README.md`](../README.md)

Internal working docs under `docs/` can stay in Chinese when they are migration-planning material.

## Current Docs

- [`legacy-backend-migration-mapping.md`](./legacy-backend-migration-mapping.md)
  - PR-1 inventory, classification, old-path to new-path mapping, capture scope list, and research/runtime boundary notes
  - Language: Chinese working doc
  - Status: `Source of truth for PR-1 migration planning`
- [`reference/legacy-backend/README.md`](./reference/legacy-backend/README.md)
  - Reserved reference-only area for selectively retained legacy research material
  - Language: Chinese working doc
  - Status: `Reference`
- [`archive/legacy-runtime/README.md`](./archive/legacy-runtime/README.md)
  - Reserved archive area for superseded legacy runtime documentation
  - Language: Chinese working doc
  - Status: `Archive`
