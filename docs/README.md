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
- [`sales-orders-projection-contract.md`](./sales-orders-projection-contract.md)
  - First `sales_orders` serving projection contract layered on top of the broader serving persistence surface
  - Language: English
  - Status: `Source of truth`
- [`capture-to-sales-orders-path.md`](./capture-to-sales-orders-path.md)
  - First minimal `capture -> transform -> serving` path for the `sales_orders` slice
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
  - Minimal transform readiness boundary and first readiness evaluator derived from the narrower admitted transform input layer
  - Language: English
  - Status: `Source of truth`
- [`transform-state-transition-boundary.md`](./transform-state-transition-boundary.md)
  - Minimal transform state-transition boundary and first narrow capture-batch lifecycle helper derived from the narrower transform readiness layer
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

- [`clean-mainline-charter.md`](./clean-mainline-charter.md)
  - Authoritative starting-point charter for the new milestone route that restarts numbering from `M1-PR1` on top of the current `main`
  - Language: Chinese working doc
  - Status: `Source of truth for the current milestone-route starting point`
- [`formal-planning-reference-boundary-and-exploration-taxonomy.md`](./formal-planning-reference-boundary-and-exploration-taxonomy.md)
  - Shared working vocabulary for the current milestone route, defining the formal/planning/reference split and the unfinished-exploration taxonomy used by follow-up planning packages
  - Language: Chinese working doc
  - Status: `Authoritative planning vocabulary for the current boundary/taxonomy baseline`
- [`legacy-backend-migration-mapping.md`](./legacy-backend-migration-mapping.md)
  - PR-1 inventory, classification, old-path to new-path mapping, capture scope list, and research/runtime boundary notes
  - Language: Chinese working doc
  - Status: `Source of truth for PR-1 migration planning`
- [`domain-migration-completeness-map.md`](./domain-migration-completeness-map.md)
  - Current planning map for database/domain migration completeness after the completed 11-package route
  - Language: Chinese working doc
  - Status: `Source of truth for current domain completeness planning`
- [`source-surface-completeness-map.md`](./source-surface-completeness-map.md)
  - Current planning map for menu, endpoint, payload-family, and slice completeness after the completed 11-package route
  - Language: Chinese working doc
  - Status: `Source of truth for current source-surface completeness planning`
- [`first-path-hardening-minimums.md`](./first-path-hardening-minimums.md)
  - Current planning note that tightens the hardening minimums for the landed first `sales_orders` capture-to-serving path
  - Language: Chinese working doc
  - Status: `Source of truth for current first-path hardening planning`
- [`post-route-mainline-planning.md`](./post-route-mainline-planning.md)
  - Historical framing note retained from the completed 11-package route and kept only as existing planning background
  - Language: Chinese working doc
  - Status: `Historical framing / existing planning asset`

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
