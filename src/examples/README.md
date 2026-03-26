# Transition Reference Patterns

This directory is a transition reference-pattern area.

It is useful for:
- isolated code sketches
- naming and layout patterns
- scoped reference-only examples that are not mounted into the app

It is not the formal home for:
- capture formal boundaries
- serving runtime boundaries
- research/reference records
- archive records

Current ownership stays explicit:
- the formal capture boundary lives under `src/app/**`, `src/migrations/**`, and the formal docs in `docs/`
- research notes, traceability samples, and troubleshooting templates belong under `docs/reference/**`
- superseded runtime context belongs under `docs/archive/**`

Anything under `src/examples/**` must stay reference-only unless a later scoped migration explicitly rewrites it into the formal layers.
