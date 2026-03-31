# Legacy Capture Bridge Note

## What This Note Is

This note is a small bridge note for the current capture migration state.

It explains how to read the current capture docs in `black-tonny-backend-base` without treating them as a statement that legacy capture has been fully migrated.

## Current Formal Surface In backend-base

The current formal capture surface in `black-tonny-backend-base` is minimal.

See:

- [Capture Minimal Boundary](./capture-minimal-boundary.md)

If the question depends on the dual-database responsibility split, also use:

- [Capture Serving Boundary](./capture-serving-boundary.md)

## Legacy Capture Reference Still Living In black-tonny-backend

Legacy capture docs and assets still living in `black-tonny-backend` remain one of the reference sources for legacy capture context.

This includes legacy capture material that has not been rewritten into the current minimal formal surface in `black-tonny-backend-base`.

## Recommended Reading Order

Read in this order:

1. Start with [Capture Minimal Boundary](./capture-minimal-boundary.md) to understand what is currently formalized in `black-tonny-backend-base`.
2. If the question depends on the dual-database responsibility split, then use [Capture Serving Boundary](./capture-serving-boundary.md).
3. If the question depends on older capture behavior, reference material, or working context, then consult the relevant legacy capture docs or assets in `black-tonny-backend`.

## Explicit Limit

This note only describes the current relationship between the new minimal formal surface and the remaining legacy capture reference.

It does not mean that legacy capture, transform, serving, admissions, or related legacy reference material have been fully migrated into `black-tonny-backend-base`.
