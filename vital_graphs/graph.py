"""Internal graph utilities (NetworkX is not part of the public API)."""

from __future__ import annotations

import networkx as nx

from vital_graphs.models.system_graph import SystemGraph


def to_networkx(graph: SystemGraph) -> nx.DiGraph[str]:
    """Build a directed graph keyed by node id with edge relation on edges."""
    g: nx.DiGraph[str] = nx.DiGraph()
    g.graph["name"] = graph.system.name
    if graph.system.description:
        g.graph["description"] = graph.system.description

    for node in graph.nodes:
        g.add_node(node.id, label=node.label)

    for edge in graph.edges:
        g.add_edge(
            edge.source,
            edge.target,
            relation=edge.relation.value,
        )

    return g
