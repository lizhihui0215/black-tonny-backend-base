# Orders First Adjacent Contract Questions

This document defines the minimum formal contract questions that a later scoped migration must answer before `black-tonny-backend-base` treats any first adjacent `/erp/orders` contract as formal repository behavior.

For the current first `sales_orders` serving projection contract that remains the only landed orders contract, use [sales-orders-projection-contract.md](./sales-orders-projection-contract.md).
For the current first minimal `capture -> transform -> serving` path that stays limited to the `sales_orders` slice, use [capture-to-sales-orders-path.md](./capture-to-sales-orders-path.md).
For the repository docs index, use [docs/README.md](./README.md).

## Current Truth

No adjacent `/erp/orders` contract is currently implemented or finalized in `black-tonny-backend-base`.

That means this document does not define adjacent contract behavior.
It only defines the minimum questions that a later scoped migration must answer explicitly instead of leaving them implicit, inherited, or assumed.

Current planning documents may inform this question list, but they are not formal truth.
Only the current repository README, docs index, formal boundary docs, and landed code/tests/migrations define current repository truth.

## What This Note Is For

This note is intentionally narrow.
It exists to make one thing explicit:
- the current repository has already narrowed one adjacent candidate route for `/erp/orders`
- that route is still only a candidate route and not a landed contract
- any future first adjacent contract package must answer a small but explicit formal question set before it may claim contract truth

This note does not provide the answers.

## Minimum Entry Conditions For The First Adjacent Contract PR

The first PR that introduces any real adjacent `/erp/orders` contract must stay narrow and must explicitly answer the minimum subset of contract questions it touches.

At minimum, that PR must state:
- what admitted input or fact grain the contract formalizes
- how target naming stays candidate-only, narrows further, or becomes formalized in that PR
- which fields are identity candidates, which are admitted non-identity fields, and which remain unresolved
- whether overwrite and upsert rules are explicitly defined by that PR or intentionally deferred
- how relation and detail-clue handling are treated in that PR
- which exclusions remain outside that PR's contract scope
- what formal-layer verification is required for the rules that PR introduces

If that first adjacent contract PR cannot answer those points explicitly, it should remain doc-only rather than imply contract behavior by omission.

## What The First Adjacent Contract PR Must Not Assume By Default

The first adjacent contract PR must not assume by default that:
- `sales_order_items-adjacent target candidate` is already the confirmed first target
- current partial carrier, relation, or detail-clue answers already equal contract truth
- downstream persistence vocabulary can silently become source-side contract vocabulary
- the first adjacent contract must reuse the `sales_orders` identity or overwrite pattern unchanged
- path shape, internal entrypoint, or behavior readiness can be inferred without being stated

## Minimum Future Contract Questions

Any later scoped migration that introduces a first adjacent `/erp/orders` contract must explicitly answer at least these questions.

### 1. Admitted Input And Fact Grain Questions

- What exact admitted input does the first adjacent contract formalize?
- Is that input one row-adjacent source-side fact shape, one normalized candidate fact shape, or something narrower?
- What is the smallest contract grain that the PR claims to persist or apply?
- Which adjacent candidate inputs remain outside the admitted contract grain?

Current boundary:
- the current repository only supports a narrowed candidate scope for the future first adjacent contract
- that narrowed scope is not yet a formal admitted input boundary

### 2. Candidate Target Naming Discipline

- What target naming does the PR use while the first adjacent target remains non-final?
- Does the PR keep a candidate-only name, or does it formalize a narrower but still non-identity contract label?
- Which names remain comparison vocabulary only?
- Which names must stay explicitly separated from contract identity?

Current boundary:
- `sales_order_items-adjacent target candidate` may inform the question set
- it must not be silently upgraded into a confirmed first target by naming alone

### 3. Identity Versus Non-Identity Field Questions

- Which admitted fields are part of the contract identity question set?
- Which admitted fields are explicitly non-identity fields even if they are required inputs?
- Which current anchor clues remain comparison clues only rather than identity inputs?
- Which fields remain unresolved and therefore cannot yet be treated as contract identity or non-identity truth?

Current boundary:
- current order-level anchors and adjacent partial answers do not yet establish contract identity
- the first adjacent contract PR must answer identity scope explicitly if it introduces any contract write rule

### 4. Overwrite And Upsert Question Set

- Does the PR define an upsert key, or does it intentionally stop short of that?
- If it defines overwrite behavior, what exact fields may be overwritten and under what matching rule?
- If overwrite is not yet formalized, what narrower contract shape is being formalized instead?
- What dedupe assumptions, if any, are required inside one contract apply call?

Current boundary:
- no overwrite or upsert rule is currently defined for any adjacent `/erp/orders` contract
- those rules must not be borrowed implicitly from `sales_orders`

### 5. Relation And Detail-Clue Treatment Questions

- How does the PR treat order-to-detail relation in formal contract terms?
- Which relation clues, if any, are formalized, and which remain comparison-only clues?
- Which detail clues, if any, are admitted into the contract question set?
- Which detail clue names remain downstream vocabulary only or unresolved source-side candidates?

Current boundary:
- current repository planning only narrows these questions into partial answers
- the first adjacent contract PR must explicitly state what remains candidate, partial, or excluded

### 6. Required Exclusions

The first adjacent contract PR must explicitly preserve the following exclusions unless that PR formally reopens them:
- payload-envelope blank or envelope-level metadata lanes
- inventory-connected lanes
- mixed multi-lane target shapes
- downgraded reference-only hints outside current formal truth

It must also state whether any additional exclusions remain necessary for that PR to stay single-theme and narrow-scope.

### 7. Verified Coverage Expectations

If the first adjacent contract PR defines any real contract rule, it must explicitly define the matching formal-layer verification.

At minimum, that PR must state:
- which admitted input cases are covered
- which identity or non-identity expectations are covered
- which overwrite or non-overwrite expectations are covered
- which exclusions are asserted by tests or doc-level verification
- which unresolved questions remain intentionally outside verified scope

If the PR cannot provide matching verification expectations, it should remain a doc-only formal-question or formal-contract sketch rather than claim implemented contract behavior.

## What Must Not Be Assumed

The later adjacent contract package must not assume by default that:
- the current candidate route already names the final target
- current partial carrier, relation, or detail-clue answers already settle source-side truth
- current persistence model fields already define contract identity
- the first adjacent contract must share the same overwrite semantics as the current `sales_orders` contract
- future path or runtime behavior can be added later without affecting the contract question set

## Non-Goals

This document does not define:
- a confirmed first adjacent target
- contract identity
- overwrite or upsert truth
- path shape
- an internal entrypoint
- behavior readiness
- a formal adjacent contract
- a formal adjacent path
- any landed runtime, schema, CRUD, service, migration, or test change

## What This Document Does Not Claim

This document does not claim that:
- an adjacent `/erp/orders` contract is already implemented
- `sales_order_items` now shares the current `sales_orders` contract pattern
- the current candidate target is already confirmed
- current partial source-accuracy answers already equal formal contract truth
- a future adjacent contract must choose one specific identity or overwrite rule

Until a later scoped migration defines explicit answers, these remain open formal contract questions rather than current repository behavior.
