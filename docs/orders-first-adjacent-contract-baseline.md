# Orders First Adjacent Contract Baseline

This document defines the current minimal formal baseline for any future first adjacent `/erp/orders` contract in `black-tonny-backend-base`.

For the current first `sales_orders` serving projection contract that remains the only landed orders contract, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the minimum future question list that a later first adjacent contract package must answer explicitly, use [orders-first-adjacent-contract-questions.md](./orders-first-adjacent-contract-questions.md).
For the current narrower scoped contract statement that stays closer to a future adjacent contract while still stopping short of implementation truth, use [orders-first-adjacent-scoped-contract-statement.md](./orders-first-adjacent-scoped-contract-statement.md).
For the current first minimal `capture -> transform -> serving` path that remains limited to the `sales_orders` slice, use [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No adjacent `/erp/orders` contract is currently implemented or finalized in `black-tonny-backend-base`.

That means this document does not define adjacent runtime behavior, adjacent write behavior, or an adjacent path.
It only defines the narrowest current formal baseline that a later first adjacent contract package must respect before any adjacent contract truth may be claimed.

Planning documents and reference material may inform this baseline, but they are not formal truth.
Only the repository README, docs index, formal boundary docs, and landed code/tests/migrations define current repository truth.

## Current Formal Baseline

The current stable formal baseline is intentionally narrow.

It already formalizes that:
- the current repository has one landed orders contract only: `sales_orders`
- any future first adjacent `/erp/orders` contract must remain narrower than a broader orders-family or multi-lane formalization
- the first adjacent contract route must stay single-theme, single-family, and narrow-scope
- current target naming remains non-final
- current identity, overwrite, upsert, path, and behavior truths are still not formalized for any adjacent contract

It does not yet formalize:
- a confirmed first adjacent target
- an adjacent contract identity
- an adjacent overwrite or upsert rule
- an adjacent path shape
- an adjacent internal entrypoint
- adjacent behavior readiness

## Admitted Contract Scope

The current formal baseline admits only one future first adjacent contract lane into scope:
- one current `/erp/orders` row-adjacent, non-`sales_orders` contract lane
- one single-theme, single-family, narrow target slice

This baseline does not yet admit:
- a multi-lane or mixed-target adjacent contract
- an envelope-level metadata contract
- an inventory-connected contract lane
- a broader `/erp/orders` family formalization

The admitted scope is therefore a route boundary, not an implemented contract.

## Target Naming Status

The current formal baseline keeps target naming intentionally non-final.

Already formalized:
- future adjacent contract work may proceed only with candidate-only target naming discipline
- current naming must stay separated from contract identity until a later scoped migration answers that boundary explicitly

Not yet formalized:
- a confirmed first adjacent target
- a final adjacent contract name
- any claim that `sales_order_items-adjacent target candidate` is already the formal first target

Candidate retained but not confirmed:
- `sales_order_items-adjacent target candidate`

## Identity And Non-Identity Status

The current formal baseline does not define adjacent contract identity.

Already formalized:
- current order-level anchors may remain comparison anchors for later adjacent contract work
- later adjacent contract work must explicitly answer identity versus non-identity field treatment instead of inheriting it silently

Not yet formalized:
- any adjacent identity field set
- any adjacent non-identity field set
- any final relation key
- any source-side detail-clue field set as contract truth

Candidate retained but not confirmed:
- current order-level anchor clues as comparison inputs only
- current partial carrier, relation, and detail-clue answers as non-final adjacent-contract inputs only

## Overwrite And Upsert Status

No overwrite or upsert rule is currently formalized for any adjacent `/erp/orders` contract.

Already formalized:
- a later adjacent contract package must answer overwrite and upsert explicitly if it introduces write behavior
- the current `sales_orders` contract pattern must not be inherited by default

Not yet formalized:
- an adjacent identity key
- an adjacent upsert key
- an adjacent dedupe rule
- an adjacent overwrite rule

## Exclusions Still Preserved

The current formal baseline preserves the following exclusions outside any future first adjacent contract unless a later scoped migration reopens them explicitly:
- payload-envelope blank or envelope-level metadata lanes
- inventory-connected lanes
- mixed multi-lane target shapes
- downgraded reference-only hints outside current formal truth

Excluded from the current contract baseline:
- broader runtime or orchestration behavior
- operator-facing behavior
- any adjacent path formalization

## Verification Expectations

The current repository has no adjacent contract-level verification because no adjacent contract is currently implemented.

The current formal baseline therefore only establishes the verification expectation for later adjacent contract work:
- a later adjacent contract package must add verification for every formal rule it introduces
- that verification must cover the admitted contract scope it formalizes
- that verification must state which identity, non-identity, overwrite, or exclusion rules are actually being claimed
- unresolved candidate or excluded lanes must remain visibly outside verified truth

Until such verification lands alongside formal rules, no adjacent contract implementation truth exists.

## Explicit Non-Goals

This document does not define:
- a confirmed first adjacent target
- contract identity
- overwrite or upsert truth
- path shape
- an internal entrypoint
- behavior readiness
- a formal adjacent path
- any landed runtime, schema, CRUD, service, migration, or test change

## What This Document Does Not Claim

This document does not claim that:
- an adjacent `/erp/orders` contract is already implemented
- the current candidate target is already confirmed
- current candidate or partial answers already equal formal contract truth
- a future adjacent contract must use one specific identity or overwrite rule
- runtime behavior, path behavior, or serving orchestration for an adjacent contract already exists

Until a later scoped migration defines explicit adjacent contract answers and lands the matching code/tests/migrations when required, this baseline remains intentionally narrow formal guidance rather than adjacent contract implementation truth.
