from __future__ import annotations

import graphviz

from vital_graphs.models.system_graph import SystemGraph


def _relation_style(relation: str) -> tuple[str, str]:
    if relation == "inhibits":
        return ("#c0392b", "tee")
    if relation == "depends_on":
        return ("#7f8c8d", "onormal")
    return ("#2c3e50", "normal")


def build_digraph(graph: SystemGraph, *, output_format: str) -> graphviz.Digraph:
    """Build a Graphviz Digraph for SVG or PNG export."""
    dot = graphviz.Digraph(
        name="vital_graphs",
        format=output_format,
        graph_attr={
            "rankdir": "LR",
            "label": graph.system.name,
            "labelloc": "t",
            "fontsize": "14",
        },
        node_attr={
            "shape": "box",
            "style": "rounded,filled",
            "fillcolor": "#ecf0f1",
            "fontname": "Helvetica",
        },
        edge_attr={"fontname": "Helvetica", "fontsize": "10"},
    )

    for node in graph.nodes:
        attrs: dict[str, str] = {"label": node.label}
        if node.fillcolor:
            attrs["fillcolor"] = node.fillcolor
        dot.node(node.id, **attrs)

    for edge in graph.edges:
        color, arrowhead = _relation_style(edge.relation.value)
        dot.edge(
            edge.source,
            edge.target,
            label=edge.relation.value,
            color=color,
            arrowhead=arrowhead,
            fontcolor=color,
        )

    return dot
