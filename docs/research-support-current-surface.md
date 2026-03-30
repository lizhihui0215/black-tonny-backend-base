# Research Support Current Surface

This note records the current formal code surface for research support in `black-tonny-backend-base`.

It is a navigation note, not a replacement for formal runtime boundary docs.

## Current Code Surface

Current research support code lives under `src/app/services/research/`:

- [`../src/app/services/research/erp_research_service.py`](../src/app/services/research/erp_research_service.py)
  - minimal aggregation contract
- [`../src/app/services/research/page_research.py`](../src/app/services/research/page_research.py)
  - minimal page research contract
- [`../src/app/services/research/menu_coverage.py`](../src/app/services/research/menu_coverage.py)
  - minimal menu coverage contract

## Current Minimal Contract

What is currently formalized:

- a minimal research support skeleton
- a minimal page research formal contract
- a minimal menu coverage formal contract
- a minimal aggregation contract that combines page research and menu coverage snapshots

## Explicit Limit

This only means the minimal formal contract and support skeleton are present.

It does not mean that any of the following have been migrated or formalized:

- legacy research logic
- route registry
- maturity board
- evidence chain
- tmp/output research assets
