from src.app.core.migration_targets import get_version_table, load_target_metadata, resolve_alembic_target


def test_resolve_alembic_target_from_explicit_target() -> None:
    assert resolve_alembic_target("capture", None) == "capture"
    assert resolve_alembic_target("serving", None) == "serving"


def test_resolve_alembic_target_from_config_filename() -> None:
    assert resolve_alembic_target(None, "/tmp/src/alembic_capture.ini") == "capture"
    assert resolve_alembic_target(None, "/tmp/src/alembic_serving.ini") == "serving"


def test_capture_metadata_is_empty() -> None:
    metadata = load_target_metadata("capture")
    assert metadata.tables == {}


def test_serving_metadata_contains_serving_tables() -> None:
    metadata = load_target_metadata("serving")
    assert {"user", "tier", "rate_limit", "token_blacklist"}.issubset(metadata.tables.keys())


def test_version_table_names_are_target_specific() -> None:
    assert get_version_table("capture") == "alembic_version_capture"
    assert get_version_table("serving") == "alembic_version_serving"
