# Legacy Research Bridge Note

## What This Note Is

This note is a small bridge note for the current research migration state.

It explains how to read the current research support docs in `black-tonny-backend-base` without treating them as a statement that legacy research has been fully migrated.

## Current Formal Surface In backend-base

The current formal research support surface in `black-tonny-backend-base` is minimal.

See:

- [Research Support Current Surface](./research-support-current-surface.md)

That current surface covers only the minimal formal contract now present under `src/app/services/research/`:

- `erp_research_service.py`
- `page_research.py`
- `menu_coverage.py`

## Legacy Research Reference Still Living In black-tonny-backend

Legacy research docs and assets still living in `black-tonny-backend` remain the reference source for legacy research context.

This includes legacy research material that has not been rewritten into the current minimal formal surface in `black-tonny-backend-base`.

## Recommended Reading Order

Read in this order:

1. Start with [Research Support Current Surface](./research-support-current-surface.md) to understand what is currently formalized in `black-tonny-backend-base`.
2. If the question depends on older research behavior, assets, or working context, then consult the relevant legacy research docs or assets in `black-tonny-backend`.

## Explicit Limit

This note only describes the current relationship between the new minimal formal surface and the remaining legacy research reference.

It does not mean that legacy research, route registry, maturity board, evidence chain, or tmp/output research assets have been fully migrated into `black-tonny-backend-base`.
