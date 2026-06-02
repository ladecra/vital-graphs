from __future__ import annotations

from dataclasses import dataclass

from vital_graphs.errors import GraphIntegrityError
from vital_graphs.models.edge import Edge, Relation
from vital_graphs.models.node import Node


@dataclass(frozen=True, slots=True)
class SystemInfo:
    name: str
    description: str | None = None


class SystemGraph:
    """Authoritative in-memory representation of a biological system."""

    def __init__(self, system: SystemInfo) -> None:
        self._system = system
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []
        self._edge_keys: set[tuple[str, str, Relation]] = set()

    @property
    def system(self) -> SystemInfo:
        return self._system

    @property
    def nodes(self) -> tuple[Node, ...]:
        return tuple(self._nodes[nid] for nid in sorted(self._nodes))

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple(self._edges)

    def add_node(self, node: Node) -> None:
        if node.id in self._nodes:
            raise GraphIntegrityError(f"duplicate node id: {node.id!r}")
        self._nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.source not in self._nodes:
            raise GraphIntegrityError(
                f"edge source {edge.source!r} is not a defined node",
            )
        if edge.target not in self._nodes:
            raise GraphIntegrityError(
                f"edge target {edge.target!r} is not a defined node",
            )
        if edge.key in self._edge_keys:
            raise GraphIntegrityError(
                f"duplicate edge: {edge.source!r} -> {edge.target!r} ({edge.relation.value})",
            )
        self._edge_keys.add(edge.key)
        self._edges.append(edge)

    def get_node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def validate_integrity(self) -> None:
        """Re-check graph invariants (no-op if graph was built only via add_*)."""
        seen_ids: set[str] = set()
        for node in self.nodes:
            if node.id in seen_ids:
                raise GraphIntegrityError(f"duplicate node id: {node.id!r}")
            seen_ids.add(node.id)

        edge_keys: set[tuple[str, str, Relation]] = set()
        for edge in self.edges:
            if edge.source not in self._nodes or edge.target not in self._nodes:
                raise GraphIntegrityError("dangling edge reference")
            if edge.key in edge_keys:
                raise GraphIntegrityError("duplicate edge")
            edge_keys.add(edge.key)
