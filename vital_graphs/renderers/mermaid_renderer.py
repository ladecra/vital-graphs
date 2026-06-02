from __future__ import annotations

from vital_graphs.models.edge import Relation
from vital_graphs.models.system_graph import SystemGraph


def _mermaid_arrow(relation: Relation) -> str:
    if relation == Relation.INHIBITS:
        return "-.->"
    return "-->"


def render_mermaid(graph: SystemGraph) -> str:
    """Return Mermaid flowchart source (no Graphviz required)."""
    lines = ["flowchart LR", f"    %% {graph.system.name}"]
    for edge in graph.edges:
        src = edge.source
        tgt = edge.target
        arrow = _mermaid_arrow(edge.relation)
        label = edge.relation.value
        lines.append(f"    {src} {arrow}|{label}| {tgt}")
    return "\n".join(lines) + "\n"
