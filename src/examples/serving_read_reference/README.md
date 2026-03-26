# Serving Read Transition Reference

This directory is a transition reference pattern for future serving-side read modules.

What it shows:
- a read-focused schema
- a router that depends on `async_get_serving_db`
- a simple SQL query pattern for read models

Important:
- this directory is not the source of truth for serving runtime contracts
- this code is not imported by the app
- it is not mounted into runtime routers
- it does not appear in `/docs`
- it is only a transition reference pattern under `src/examples/`
- adapt the query shape and naming only after deciding a formal serving home outside `src/examples/`
