from src.app.services.research.menu_coverage import MenuCoverageSnapshot


def test_menu_coverage_snapshot_uses_conservative_defaults() -> None:
    snapshot = MenuCoverageSnapshot(
        source_name="yeusoft.research",
        menu_key="report-root",
    )

    assert snapshot.source_name == "yeusoft.research"
    assert snapshot.menu_key == "report-root"
    assert snapshot.menu_title is None
    assert snapshot.coverage_status == "stub"
    assert snapshot.notes == ()


def test_menu_coverage_snapshot_allows_thin_title_and_status_fields() -> None:
    snapshot = MenuCoverageSnapshot(
        source_name="yeusoft.research",
        menu_key="report-root",
        menu_title="报表管理",
        coverage_status="noted",
        notes=("manual note exists",),
    )

    assert snapshot.menu_title == "报表管理"
    assert snapshot.coverage_status == "noted"
    assert snapshot.notes == ("manual note exists",)
