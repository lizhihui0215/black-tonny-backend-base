# Serving Read Reference

This directory is a reference-only example for future serving-side read modules.

What it shows:
- a read-focused schema
- a router that depends on `async_get_serving_db`
- a simple SQL query pattern for read models

Important:
- this code is not imported by the app
- it is not mounted into runtime routers
- it does not appear in `/docs`
- adapt the query shape and naming before using it in a real serving module
