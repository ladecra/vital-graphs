from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Relation(StrEnum):
    STIMULATES = "stimulates"
    INHIBITS = "inhibits"
    REGULATES = "regulates"
    DEPENDS_ON = "depends_on"


@dataclass(frozen=True, slots=True)
class Edge:
    """A directed relationship between two nodes."""

    source: str
    target: str
    relation: Relation

    @property
    def key(self) -> tuple[str, str, Relation]:
        return (self.source, self.target, self.relation)
