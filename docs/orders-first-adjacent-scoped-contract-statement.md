# Orders First Adjacent Scoped Contract Statement

This document defines the current narrow formal scoped contract statement for any future first adjacent `/erp/orders` contract in `black-tonny-backend-base`.

For the current minimal formal baseline that still stops short of any adjacent contract implementation, use [orders-first-adjacent-contract-baseline.md](./orders-first-adjacent-contract-baseline.md).
For the minimum future question list that a later first adjacent contract package must answer explicitly, use [orders-first-adjacent-contract-questions.md](./orders-first-adjacent-contract-questions.md).
For the current first `sales_orders` serving projection contract that remains the only landed orders contract, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No adjacent `/erp/orders` contract is currently implemented or finalized in `black-tonny-backend-base`.

That means this document does not define adjacent runtime behavior, adjacent writes, or any adjacent path behavior.
It only defines the narrowest current scoped contract statement that a later first adjacent contract package may build on before any adjacent implementation truth is claimed.

Planning documents may inform this scoped statement, but they are not formal truth.
Only the repository README, docs index, formal boundary docs, and landed code/tests/migrations define current repository truth.

## Current Scoped Contract Statement

The current scoped contract statement is intentionally narrow.

Already formalized in this scoped statement:
- any future first adjacent `/erp/orders` contract must remain outside the already landed `sales_orders` slice
- any future first adjacent contract must stay limited to one row-adjacent, non-`sales_orders` contract lane
- that lane must stay single-theme, single-family, and narrow-scope
- current target naming inside that lane remains candidate-only and non-final
- current source-side carrier, relation, and detail-clue inputs remain non-final contract inputs rather than adjacent contract truth

Not yet formalized in this scoped statement:
- a confirmed first adjacent target
- an adjacent contract identity
- an adjacent overwrite or upsert rule
- an adjacent path shape
- an adjacent internal entrypoint
- adjacent runtime or behavior truth

If current evidence ever stops supporting this narrow scoped statement safely, the contract route must remain at baseline-only truth instead of over-claiming contract formalization.

## Admitted Contract Scope

The current scoped contract statement admits only this future adjacent contract scope:
- one current `/erp/orders` row-adjacent, non-`sales_orders` lane
- one order-attached detail-facts contract neighborhood
- one narrow candidate target neighborhood

Already formalized in scope:
- the first adjacent contract route cannot widen into a broader `/erp/orders` family statement
- the first adjacent contract route cannot widen into multiple target lanes
- the first adjacent contract route cannot collapse target naming, identity, and behavior into one step

Excluded from the current scoped contract statement:
- envelope-level metadata lanes
- inventory-connected lanes
- mixed multi-lane target shapes
- broader runtime or orchestration behavior
- any adjacent path formalization

## Target Naming Status

The current scoped contract statement keeps target naming explicitly non-final.

Already formalized in the scoped statement:
- future adjacent contract work may only use candidate-only target naming discipline
- target naming must remain separate from contract identity

Candidate retained but not confirmed:
- `sales_order_items-adjacent target candidate`
- one order-attached detail-facts candidate neighborhood

Not yet formalized:
- a confirmed first adjacent target
- a final adjacent contract name
- any claim that a candidate target name is already adjacent contract truth

## Identity And Non-Identity Status

The current scoped contract statement does not define adjacent identity or adjacent non-identity field truth.

Already formalized in the scoped statement:
- current order-level anchors may remain comparison anchors only
- current carrier, relation, and detail-clue outputs may remain non-final contract inputs only
- a later adjacent contract package must answer identity versus non-identity treatment explicitly if it introduces any real contract write rule

Candidate retained but not confirmed:
- current order-level anchor clues as comparison inputs
- current partial carrier answer as contract-scope input only
- current partial relation answer as contract-scope input only
- current partial detail-clue answer as contract-scope input only

Not yet formalized:
- any adjacent identity field set
- any adjacent non-identity field set
- any final relation key
- any detail clue set as adjacent contract truth

## Overwrite And Upsert Status

No overwrite or upsert rule is currently formalized for any adjacent `/erp/orders` contract.

Already formalized in the scoped statement:
- a later adjacent contract package must answer overwrite and upsert explicitly before claiming adjacent write truth
- the current `sales_orders` contract pattern must not be inherited by default

Not yet formalized:
- an adjacent identity key
- an adjacent upsert key
- an adjacent dedupe rule
- an adjacent overwrite rule

## Exclusions Still Preserved

The current scoped contract statement preserves the following exclusions outside any future first adjacent contract unless a later scoped migration reopens them explicitly:
- payload-envelope blank or envelope-level metadata lanes
- inventory-connected lanes
- mixed multi-lane target shapes
- downgraded reference-only hints outside current formal truth

Excluded from the current scoped contract statement:
- formal adjacent path truth
- broader runtime behavior
- operator-facing behavior
- any implication that current reference or planning inputs are already adjacent implementation truth

## Verification Expectations

The current repository has no adjacent contract-level verification because no adjacent contract is currently implemented.

The current scoped contract statement therefore only formalizes the verification expectation for later adjacent contract work:
- a later adjacent contract package must add verification for every formal rule it introduces
- verification must stay aligned to the admitted contract scope claimed by that package
- verification must state which identity, non-identity, overwrite, exclusion, or candidate-retention boundaries are being claimed
- unresolved candidate or excluded lanes must remain outside verified truth

Until that verification lands with matching formal rules, no adjacent contract implementation truth exists.

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
- current candidate or partial answers already equal adjacent contract truth
- a future adjacent contract must use one specific identity or overwrite rule
- runtime behavior, path behavior, or serving orchestration for an adjacent contract already exists

Until a later scoped migration defines explicit adjacent contract answers and lands the matching code/tests/migrations when required, this scoped contract statement remains intentionally narrow formal guidance rather than adjacent contract implementation truth.
