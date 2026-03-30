import ast
from pathlib import Path

import pytest

from src.app.services.research import (
    ERPResearchService,
    ERPResearchSupportSnapshot,
    MenuCoverageSnapshot,
    PageResearchSnapshot,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_FILES = (
    REPO_ROOT / "src/app/services/research/erp_research_service.py",
    REPO_ROOT / "src/app/services/research/page_research.py",
    REPO_ROOT / "src/app/services/research/menu_coverage.py",
)
BANNED_IMPORT_PREFIXES = (
    "src.app.api",
    "src.app.crud",
    "src.app.models",
    "src.app.schemas",
    "src.app.services.capture_write",
    "src.app.services.serving",
    "src.app.services.transform",
    "src.app.worker",
)


def _import_targets(module_path: Path) -> set[str]:
    parsed = ast.parse(module_path.read_text(encoding="utf-8"))
    targets: set[str] = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for alias in node.names:
                targets.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                targets.add(node.module)
    return targets


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


def test_research_support_modules_export_minimal_public_objects() -> None:
    assert ERPResearchService is not None
    assert ERPResearchSupportSnapshot is not None
    assert PageResearchSnapshot is not None
    assert MenuCoverageSnapshot is not None


@pytest.mark.asyncio
async def test_research_service_collects_minimal_support_snapshot() -> None:
    service = ERPResearchService(
        page_research_support=_FakePageResearchSupport(),
        menu_coverage_support=_FakeMenuCoverageSupport(),
    )

    snapshot = await service.collect_support_snapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
        menu_key="report-root",
    )

    assert isinstance(snapshot, ERPResearchSupportSnapshot)
    assert snapshot.source_name == "yeusoft.research"
    assert snapshot.page_research == PageResearchSnapshot(
        source_name="yeusoft.research",
        page_key="sales-detail",
        notes=("page skeleton",),
    )
    assert snapshot.menu_coverage == MenuCoverageSnapshot(
        source_name="yeusoft.research",
        menu_key="report-root",
        notes=("menu skeleton",),
    )


def test_research_support_skeleton_does_not_import_runtime_or_capture_layers() -> None:
    imported_modules = {target for path in RESEARCH_FILES for target in _import_targets(path)}

    assert imported_modules
    for banned_prefix in BANNED_IMPORT_PREFIXES:
        assert all(not target.startswith(banned_prefix) for target in imported_modules)
