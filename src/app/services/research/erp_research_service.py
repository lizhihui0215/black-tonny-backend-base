from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .menu_coverage import MenuCoverageSnapshot, MenuCoverageSupport
from .page_research import PageResearchSnapshot, PageResearchSupport

ERPResearchAggregationStatus = Literal["stub", "partial", "collected"]


@dataclass(frozen=True, slots=True)
class ERPResearchSupportSnapshot:
    """Minimal combined non-runtime snapshot for research support."""

    source_name: str
    page_research: PageResearchSnapshot | None = None
    menu_coverage: MenuCoverageSnapshot | None = None
    aggregation_status: ERPResearchAggregationStatus = "stub"


@dataclass(slots=True)
class ERPResearchService:
    """Minimal orchestration entry for future research support work."""

    page_research_support: PageResearchSupport
    menu_coverage_support: MenuCoverageSupport

    async def collect_support_snapshot(
        self,
        *,
        source_name: str,
        page_key: str | None = None,
        menu_key: str | None = None,
    ) -> ERPResearchSupportSnapshot:
        page_research = None
        if page_key is not None:
            page_research = await self.page_research_support.describe_page(
                source_name=source_name,
                page_key=page_key,
            )

        menu_coverage = None
        if menu_key is not None:
            menu_coverage = await self.menu_coverage_support.describe_menu_coverage(
                source_name=source_name,
                menu_key=menu_key,
            )

        aggregation_status: ERPResearchAggregationStatus = "stub"
        if page_research is not None and menu_coverage is not None:
            aggregation_status = "collected"
        elif page_research is not None or menu_coverage is not None:
            aggregation_status = "partial"

        return ERPResearchSupportSnapshot(
            source_name=source_name,
            page_research=page_research,
            menu_coverage=menu_coverage,
            aggregation_status=aggregation_status,
        )
