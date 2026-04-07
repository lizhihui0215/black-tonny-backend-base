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
- [`orders-first-adjacent-contract-questions.md`](./orders-first-adjacent-contract-questions.md)
  - Minimum future question list that a scoped first adjacent `/erp/orders` contract must answer explicitly
  - Language: English
  - Status: `Source of truth`
- [`orders-first-adjacent-contract-baseline.md`](./orders-first-adjacent-contract-baseline.md)
  - Current minimal formal baseline for any future first adjacent `/erp/orders` contract while no adjacent contract is yet implemented
  - Language: English
  - Status: `Source of truth`
- [`orders-first-adjacent-scoped-contract-statement.md`](./orders-first-adjacent-scoped-contract-statement.md)
  - Current narrow formal scoped contract statement for the future first adjacent `/erp/orders` contract while no adjacent contract is yet implemented
  - Language: English
  - Status: `Source of truth`
- [`orders-first-adjacent-contract-implementation-preflight.md`](./orders-first-adjacent-contract-implementation-preflight.md)
  - Current minimal formal implementation-preflight slice for the future first adjacent `/erp/orders` contract while no adjacent contract is yet implemented
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

- [`source-intelligence/README.md`](./source-intelligence/README.md)
  - Entry index and minimal output structure for the new source-intelligence docs subtree, separating current output slots from older upstream input docs
  - Language: Chinese working doc
  - Status: `Current source-intelligence docs structure index`
- [`source-intelligence/ops/README.md`](./source-intelligence/ops/README.md)
  - Review, handoff, milestone, and quality-gate control-plane entry for the source-intelligence subtree; not a new dossier/field/relation/readiness output slot
  - Language: Chinese working doc
  - Status: `Current source-intelligence ops control-plane entry`
- [`source-intelligence/migration-charter.md`](./source-intelligence/migration-charter.md)
  - Authoritative entry charter for the new source-intelligence mainline, defining migration target, evidence taxonomy, legacy-asset classification, deliverable types, and review guardrails
  - Language: Chinese working doc
  - Status: `Source of truth for the current source-intelligence route starting point`
- [`source-intelligence/legacy-source-intelligence-inventory-baseline.md`](./source-intelligence/legacy-source-intelligence-inventory-baseline.md)
  - First legacy source-intelligence inventory baseline, classifying which legacy knowledge assets are worth migrating next and what new-repo asset types they should become
  - Language: Chinese working doc
  - Status: `Current source-intelligence legacy inventory baseline`
- [`source-intelligence/apis/erp-orders-api-dossier.md`](./source-intelligence/apis/erp-orders-api-dossier.md)
  - First real source-intelligence API dossier sample for `/erp/orders`, rewriting current repo-owned endpoint knowledge into a reusable dossier structure with explicit evidence levels
  - Language: Chinese working doc
  - Status: `Current source-intelligence API dossier sample`
- [`source-intelligence/apis/sales-list-selsalereport-api-dossier.md`](./source-intelligence/apis/sales-list-selsalereport-api-dossier.md)
  - Second real source-intelligence API dossier sample, rewriting the legacy `sales list family` primary head endpoint `SelSaleReport` into a single-endpoint dossier while keeping the broader family out of scope
  - Language: Chinese working doc
  - Status: `Current source-intelligence API dossier sample`
- [`source-intelligence/apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md`](./source-intelligence/apis/sales-list-getdiyreportdata-e004001008-2-api-dossier.md)
  - Third real source-intelligence API dossier sample, rewriting the legacy `sales list family` line-side object `GetDIYReportData(E004001008_2)` into a single-object dossier without expanding into a whole family graph
  - Language: Chinese working doc
  - Status: `Current source-intelligence API dossier sample`
- [`source-intelligence/fields/erp-orders-first-slice-field-dictionary.md`](./source-intelligence/fields/erp-orders-first-slice-field-dictionary.md)
  - First real source-intelligence field dictionary sample for `/erp/orders`, covering the narrow first-slice fields that already carry the highest current serving value
  - Language: Chinese working doc
  - Status: `Current source-intelligence field dictionary sample`
- [`source-intelligence/fields/selsalereport-core-field-dictionary.md`](./source-intelligence/fields/selsalereport-core-field-dictionary.md)
  - First real source-intelligence field dictionary sample for `SelSaleReport`, covering a narrow head-like core field cluster without expanding into a whole sales-family glossary
  - Language: Chinese working doc
  - Status: `Current source-intelligence field dictionary sample`
- [`source-intelligence/fields/sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md`](./source-intelligence/fields/sales-list-getdiyreportdata-e004001008-2-core-field-dictionary.md)
  - Third real source-intelligence field dictionary sample, covering a narrow line-side core field cluster for `GetDIYReportData(E004001008_2)` without expanding into a whole line glossary
  - Language: Chinese working doc
  - Status: `Current source-intelligence field dictionary sample`
- [`source-intelligence/relations/erp-orders-first-slice-relation-doc.md`](./source-intelligence/relations/erp-orders-first-slice-relation-doc.md)
  - First real source-intelligence relation doc sample for `/erp/orders`, covering narrow first-slice field relations, injected-context boundaries, and conservative adjacent clue relation status
  - Language: Chinese working doc
  - Status: `Current source-intelligence relation doc sample`
- [`source-intelligence/relations/selsalereport-head-line-boundary-relation-doc.md`](./source-intelligence/relations/selsalereport-head-line-boundary-relation-doc.md)
  - First real source-intelligence relation doc sample for the `SelSaleReport` line, covering the narrow head-line boundary without expanding into a whole sales-family relation map
  - Language: Chinese working doc
  - Status: `Current source-intelligence relation doc sample`
- [`source-intelligence/serving-readiness/erp-orders-first-slice-serving-readiness.md`](./source-intelligence/serving-readiness/erp-orders-first-slice-serving-readiness.md)
  - First real source-intelligence serving-readiness sample for `/erp/orders`, defining what is ready now for the current first `sales_orders` slice and what still cannot be upgraded
  - Language: Chinese working doc
  - Status: `Current source-intelligence serving-readiness sample`
- [`source-intelligence/serving-readiness/selsalereport-head-slice-serving-readiness.md`](./source-intelligence/serving-readiness/selsalereport-head-slice-serving-readiness.md)
  - First real source-intelligence serving-readiness sample for `SelSaleReport`, defining what is ready now for the narrow head slice and why that still cannot be promoted into line-side, reconciliation, or whole-family readiness
  - Language: Chinese working doc
  - Status: `Current source-intelligence serving-readiness sample`
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
  - Current planning baseline for repo-owned menu/page/endpoint/payload-family inventory on top of the current `main`
  - Language: Chinese working doc
  - Status: `Current planning baseline for repo-owned source inventory / source-surface mapping`
- [`orders-adjacent-payload-family-baseline.md`](./orders-adjacent-payload-family-baseline.md)
  - Current planning baseline for the current `/erp/orders` line's adjacent payload-family candidates outside the landed `sales_orders` first slice
  - Language: Chinese working doc
  - Status: `Current planning baseline for /erp/orders adjacent payload-family candidates`
- [`orders-adjacent-payload-semantics-baseline.md`](./orders-adjacent-payload-semantics-baseline.md)
  - Current planning baseline for candidate semantics, pending semantics, and unresolved ambiguities inside the current `/erp/orders` line's named payload families
  - Language: Chinese working doc
  - Status: `Current planning baseline for /erp/orders adjacent payload semantics`
- [`orders-adjacent-contract-entry-minimums.md`](./orders-adjacent-contract-entry-minimums.md)
  - Current planning baseline for the minimum family / semantics / evidence / mapping / boundary conditions required before the first adjacent `/erp/orders` contract/path package may open
  - Language: Chinese working doc
  - Status: `Current planning baseline for /erp/orders adjacent contract-entry minimums`
- [`orders-source-accuracy-minimums.md`](./orders-source-accuracy-minimums.md)
  - Current planning baseline for the source-accuracy minimums that the current `/erp/orders` line must answer before adjacent contract-entry may be revisited
  - Language: Chinese working doc
  - Status: `Current planning baseline for /erp/orders source-accuracy minimums`
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
