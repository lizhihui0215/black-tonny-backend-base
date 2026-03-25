# Capture CRUD Reference

This directory is a reference-only example for future capture-side modules.

What it shows:
- a minimal SQLAlchemy model
- matching Pydantic schemas
- a FastCRUD declaration
- a router that depends on `async_get_capture_db`

Important:
- this code is not imported by the app
- it is not mounted into runtime routers
- it does not appear in `/docs`
- copy and rename it before using it in real business modules
