# Orders First Adjacent Contract Implementation Preflight

This document defines the current minimal formal implementation-preflight slice for any future first adjacent `/erp/orders` contract in `black-tonny-backend-base`.

For the minimum future question list that a later first adjacent contract package must answer explicitly, use [orders-first-adjacent-contract-questions.md](./orders-first-adjacent-contract-questions.md).
For the current minimal formal baseline that still stops short of any adjacent contract implementation, use [orders-first-adjacent-contract-baseline.md](./orders-first-adjacent-contract-baseline.md).
For the current narrow formal scoped contract statement that stays closer to a future adjacent contract while still stopping short of implementation truth, use [orders-first-adjacent-scoped-contract-statement.md](./orders-first-adjacent-scoped-contract-statement.md).
For the current first `sales_orders` serving projection contract that remains the only landed orders contract, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the planning-only adjacent route chain that informs this note without defining formal truth, start from [orders-first-adjacent-contract-prep-preflight.md](./orders-first-adjacent-contract-prep-preflight.md) and [orders-source-accuracy-revisit.md](./orders-source-accuracy-revisit.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No adjacent `/erp/orders` contract is currently implemented or finalized in `black-tonny-backend-base`.

That means this document does not define adjacent runtime behavior, adjacent write behavior, or an adjacent path.
It only defines whether the current repository already admits one minimal docs-plus-code implementation-preflight slice and one narrower contract-prep anchor slice without claiming adjacent contract truth.

Planning documents may inform this note, but they are not formal truth.
Only the repository README, docs index, formal boundary docs, and landed code/tests/migrations define current repository truth.

## Current Preflight Answer

One minimal, reversible implementation-preflight slice now exists.

That preflight slice is intentionally narrow:
- it may document and anchor one preflight-only service-layer touchpoint for a future first adjacent `/erp/orders` contract route
- it may reuse the current `sales_order_items` persistence surface as comparison-only anchor code
- it may add one preflight-oriented docs/code verification file
- it must still stop short of adjacent contract identity, overwrite, upsert, path, or behavior truth

This remains an implementation-preflight answer only.
It is not an adjacent contract implementation answer.

## Current Contract-Prep Anchor Answer

The current preflight-only service anchor may narrow one step further into one contract-prep anchor.

That contract-prep anchor is narrower than the broader implementation-preflight slice:
- it is non-writing
- it is non-migrating
- it is non-runtime-binding
- it keeps `sales_order_items-adjacent target candidate` as candidate-only
- it formalizes only the smallest allowed anchor surface that a later adjacent contract package may hang on

This anchor formalizes only:
- one anchor name: `orders_first_adjacent_contract_prep_anchor`
- one anchor file: `src/app/services/orders_first_adjacent_contract_implementation_preflight.py`
- one candidate-only target neighborhood
- one minimal allowed comparison-anchor set
- one remaining blocker list
- one forbidden-truth list

This anchor does not formalize:
- an adjacent contract helper
- an adjacent write helper
- an adjacent path helper
- runtime wiring
- migration requirements

This is the narrowest anchor surface currently admitted by formal truth.
If later work cannot remain inside this anchor without defining forbidden truths, it should stop at docs-only or move to true adjacent contract package judgment instead of widening anchor-only code.

## Minimal Allowed Dependencies

### Formal Inputs Reused But Not Reopened

The current contract-prep anchor may reuse only these direct formal inputs:
- `docs/orders-first-adjacent-contract-questions.md`
- `docs/orders-first-adjacent-contract-baseline.md`
- `docs/orders-first-adjacent-scoped-contract-statement.md`

These documents remain formal question, baseline, and scoped-contract anchors only.
The current contract-prep anchor must not reopen them into identity, overwrite, upsert, path, or behavior truth.

### Minimal Comparison Anchors

The current contract-prep anchor may depend only on these comparison anchors:
- `src/app/models/sales_order_item.py`
- `src/app/schemas/sales.py`
- `src/app/crud/crud_sales_order_items.py`

These comparison anchors are admitted only because they already expose the narrow current `sales_order_items` persistence surface.
They do not confirm a first adjacent target.
They do not confirm an adjacent identity.
They do not confirm adjacent write behavior.

No broader comparison-anchor set is admitted by this slice.
That means the current contract-prep anchor must not depend on:
- any adjacent write helper
- any adjacent path helper
- runtime routers or runtime dependency wiring
- migrations as anchor prerequisites
- inventory, orchestration, or operator-facing surfaces

## Permitted Touch Surface

The current contract-prep anchor slice may touch only the following file types.

### Formal Docs

The current contract-prep anchor slice may update only this document unless a directly adjacent formal document must be touched to prevent contradiction.

### Code

The current contract-prep anchor slice may modify only:
- `src/app/services/orders_first_adjacent_contract_implementation_preflight.py`

That file may expose:
- one implementation-preflight summary getter
- one narrower contract-prep anchor getter

That file must not expose:
- an adjacent write helper
- an adjacent apply helper
- an adjacent path helper
- runtime registration or runtime binding

### Tests

The current contract-prep anchor slice may add or update only one preflight/anchor-oriented verification file:
- `tests/test_orders_first_adjacent_contract_implementation_preflight.py`

That verification may assert only the currently admitted preflight and contract-prep anchor boundaries.
It must not assert adjacent contract behavior.

### Migrations

Migrations stay unchanged by default for this contract-prep anchor slice.

The current repository still does not prove that a migration is required just to admit this narrower contract-prep anchor.
A migration may become a blocker conclusion only if a later narrower package proves that no safe adjacent contract slice exists without an identity or write constraint.
That proof does not currently exist in formal repository truth.

## Current Code-Surface Judgment

The current code surface is narrow enough to admit one contract-prep anchor because:
- `sales_orders` remains the only landed orders contract
- `sales_order_items` still exists only as a persistence surface with model, schema, CRUD, and table migration coverage
- no adjacent `/erp/orders` contract helper, adjacent path helper, or adjacent write constraint is currently implemented
- the current contract-prep anchor may rely only on comparison anchors and forbidden-truth boundaries

The current code surface is not narrow enough to admit a real adjacent contract helper because:
- `sales_order_items-adjacent target candidate` still remains candidate-only
- current carrier, relation, and detail-clue answers remain partial or comparison-only inputs
- no adjacent identity, overwrite rule, upsert key, or internal path truth is formalized

## Current Blockers To A Real Adjacent Contract Helper

The following blockers still prevent this contract-prep anchor from becoming a real adjacent contract helper:
- `sales_order_items-adjacent target candidate` is not yet a confirmed first adjacent target
- source-side carrier truth is not yet formalized for the adjacent lane
- order-to-detail relation truth is not yet formalized for the adjacent lane
- source-side detail-clue truth is not yet formalized for the adjacent lane
- adjacent identity versus non-identity fields are not yet formalized
- adjacent overwrite and upsert rules are not yet formalized
- no adjacent path shape or behavior readiness is yet formalized

Until those blockers are answered by a later scoped package, this repository only admits the current contract-prep anchor and not a real adjacent contract helper.

## Truths That This Slice Must Not Define

The current contract-prep anchor slice must not define:
- a confirmed first adjacent target
- adjacent identity truth
- adjacent non-identity field truth
- adjacent overwrite or upsert truth
- adjacent write-helper truth
- adjacent path-helper truth
- adjacent runtime-binding truth
- adjacent migration-requirement truth

If a later change needs any of those truths to stay self-consistent, it is already outside this contract-prep anchor slice.

## Current Verified Coverage

The current implementation-preflight and contract-prep anchor slice is verified only at the docs/code boundary.

The current verification file is:
- `tests/test_orders_first_adjacent_contract_implementation_preflight.py`

That file verifies:
- this document stays aligned with the narrower contract-prep anchor boundary
- the preflight-only service-layer anchor remains non-writing, non-migrating, and non-runtime-binding
- the narrower contract-prep anchor exposes only the minimal allowed comparison anchors
- the `sales_order_items` code surface remains comparison-only in this slice

## What This Document Does Not Claim

This document does not claim that:
- an adjacent `/erp/orders` contract is already implemented
- `sales_order_items` is already the confirmed first adjacent target
- the current contract-prep anchor is already the final internal contract entrypoint
- adjacent identity, overwrite, or upsert truth already exists
- an adjacent path or behavior implementation already exists
- a migration is already required for the current contract-prep anchor slice
