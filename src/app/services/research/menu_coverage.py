from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class MenuCoverageSnapshot:
    """Minimal non-runtime snapshot for menu coverage support."""

    source_name: str
    menu_key: str
    notes: tuple[str, ...] = ()


class MenuCoverageSupport(Protocol):
    """Thin menu coverage support interface for future non-runtime implementations."""

    async def describe_menu_coverage(
        self,
        *,
        source_name: str,
        menu_key: str,
    ) -> MenuCoverageSnapshot: ...
