from src.app.core.migration_targets import get_version_table, load_target_metadata, resolve_alembic_target


def test_resolve_alembic_target_from_explicit_target() -> None:
    assert resolve_alembic_target("capture", None) == "capture"
    assert resolve_alembic_target("serving", None) == "serving"


def test_resolve_alembic_target_from_config_filename() -> None:
    assert resolve_alembic_target(None, "/tmp/src/alembic_capture.ini") == "capture"
    assert resolve_alembic_target(None, "/tmp/src/alembic_serving.ini") == "serving"


def test_capture_metadata_contains_minimal_capture_tables() -> None:
    metadata = load_target_metadata("capture")
    assert {"analysis_batches", "capture_batches", "capture_endpoint_payloads"}.issubset(metadata.tables.keys())


def test_capture_metadata_excludes_serving_tables() -> None:
    metadata = load_target_metadata("capture")
    assert "user" not in metadata.tables
    assert "tier" not in metadata.tables
    assert "rate_limit" not in metadata.tables
    assert "token_blacklist" not in metadata.tables


def test_serving_metadata_contains_serving_tables() -> None:
    metadata = load_target_metadata("serving")
    assert {"user", "tier", "rate_limit", "token_blacklist", "sales_orders", "sales_order_items"}.issubset(
        metadata.tables.keys()
    )


def test_serving_metadata_excludes_capture_tables() -> None:
    metadata = load_target_metadata("serving")
    assert "analysis_batches" not in metadata.tables
    assert "capture_batches" not in metadata.tables
    assert "capture_endpoint_payloads" not in metadata.tables


def test_version_table_names_are_target_specific() -> None:
    assert get_version_table("capture") == "alembic_version_capture"
    assert get_version_table("serving") == "alembic_version_serving"
