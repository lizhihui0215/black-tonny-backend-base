import pytest

from src.app.services.research.erp_research_service import ERPResearchService, ERPResearchSupportSnapshot
from src.app.services.research.menu_coverage import MenuCoverageSnapshot
from src.app.services.research.page_research import PageResearchSnapshot


class _FakePageResearchSupport:
    async def describe_page(self, *, source_name: str, page_key: str) -> PageResearchSnapshot:
        return PageResearchSnapshot(
            source_name=source_name,
            page_key=page_key,
            notes=("page skeleton",),
        )


class _FakeMenuCoverageSupport:
    async def describe_menu_coverage(self, *, source_name: str, menu_key: str) -> MenuCoverageSnapshot:
        return MenuCoverageSnapshot(
            source_name=source_name,
            menu_key=menu_key,
            notes=("menu skeleton",),
        )


@pytest.mark.asyncio
async def test_collect_support_snapshot_uses_stub_status_when_no_child_snapshot_is_requested() -> None:
    service = ERPResearchService(
        page_research_support=_FakePageResearchSupport(),
        menu_coverage_support=_FakeMenuCoverageSupport(),
    )

    snapshot = await service.collect_support_snapshot(source_name="yeusoft.research")

    assert snapshot == ERPResearchSupportSnapshot(
        source_name="yeusoft.research",
        aggregation_status="stub",
    )


@pytest.mark.asyncio
async def test_collect_support_snapshot_uses_partial_status_when_only_one_child_snapshot_exists() -> None:
    service = ERPResearchService(
        page_research_support=_FakePageResearchSupport(),
        menu_coverage_support=_FakeMenuCoverageSupport(),
    )

    snapshot = await service.collect_support_snapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
    )

    assert snapshot == ERPResearchSupportSnapshot(
        source_name="yeusoft.research",
        page_research=PageResearchSnapshot(
            source_name="yeusoft.research",
            page_key="sales-detail",
            notes=("page skeleton",),
        ),
        aggregation_status="partial",
    )


@pytest.mark.asyncio
async def test_collect_support_snapshot_uses_collected_status_when_both_child_snapshots_exist() -> None:
    service = ERPResearchService(
        page_research_support=_FakePageResearchSupport(),
        menu_coverage_support=_FakeMenuCoverageSupport(),
    )

    snapshot = await service.collect_support_snapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
        menu_key="report-root",
    )

    assert snapshot == ERPResearchSupportSnapshot(
        source_name="yeusoft.research",
        page_research=PageResearchSnapshot(
            source_name="yeusoft.research",
            page_key="sales-detail",
            notes=("page skeleton",),
        ),
        menu_coverage=MenuCoverageSnapshot(
            source_name="yeusoft.research",
            menu_key="report-root",
            notes=("menu skeleton",),
        ),
        aggregation_status="collected",
    )
