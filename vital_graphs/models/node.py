from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Node:
    """A vertex in a biological system graph."""

    id: str
    label: str
    fillcolor: str | None = None
