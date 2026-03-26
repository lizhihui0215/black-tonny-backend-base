# Capture CRUD Transition Reference

This directory is a transition reference pattern for capture-side modules.

The formal capture contract already lives under:
- `src/app/models/`
- `src/app/schemas/`
- `src/app/crud/`
- `src/migrations/capture_versions/`

What it shows:
- a minimal SQLAlchemy model
- matching Pydantic schemas
- a FastCRUD declaration
- a router that depends on `async_get_capture_db`

Important:
- this directory is not the source of truth for capture
- this code is not imported by the app
- it is not mounted into runtime routers
- it does not appear in `/docs`
- it is only a transition reference pattern under `src/examples/`
- future scoped capture work should start from the formal contract under `src/app/**`, not by treating this directory as capture's long-term home
