from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

MenuCoverageStatus = Literal["stub", "noted"]


@dataclass(frozen=True, slots=True)
class MenuCoverageSnapshot:
    """Minimal non-runtime snapshot for menu coverage support."""

    source_name: str
    menu_key: str
    menu_title: str | None = None
    coverage_status: MenuCoverageStatus = "stub"
    notes: tuple[str, ...] = ()


class MenuCoverageSupport(Protocol):
    """Thin menu coverage support interface for future non-runtime implementations."""

    async def describe_menu_coverage(
        self,
        *,
        source_name: str,
        menu_key: str,
    ) -> MenuCoverageSnapshot: ...
