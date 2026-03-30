from src.app.services.research.page_research import PageResearchSnapshot


def test_page_research_snapshot_uses_conservative_defaults() -> None:
    snapshot = PageResearchSnapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
    )

    assert snapshot.source_name == "yeusoft.research"
    assert snapshot.page_key == "sales-detail"
    assert snapshot.page_title is None
    assert snapshot.research_status == "stub"
    assert snapshot.notes == ()


def test_page_research_snapshot_allows_thin_title_and_status_fields() -> None:
    snapshot = PageResearchSnapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
        page_title="销售明细统计",
        research_status="noted",
        notes=("manual note exists",),
    )

    assert snapshot.page_title == "销售明细统计"
    assert snapshot.research_status == "noted"
    assert snapshot.notes == ("manual note exists",)
