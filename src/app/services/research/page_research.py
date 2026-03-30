from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PageResearchSnapshot:
    """Minimal non-runtime snapshot for page research support."""

    source_name: str
    page_key: str
    notes: tuple[str, ...] = ()


class PageResearchSupport(Protocol):
    """Thin page research support interface for future non-runtime implementations."""

    async def describe_page(
        self,
        *,
        source_name: str,
        page_key: str,
    ) -> PageResearchSnapshot: ...
