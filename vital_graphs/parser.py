from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from vital_graphs.errors import ValidationError
from vital_graphs.models.edge import Edge, Relation
from vital_graphs.models.node import Node
from vital_graphs.models.system_graph import SystemGraph, SystemInfo
from vital_graphs.validators.schema import validate_document


def load(source: str | Path) -> SystemGraph:
    """Load a YAML file into a SystemGraph."""
    path = Path(source)
    if not path.is_file():
        raise ValidationError(f"file not found: {path}")

    try:
        data: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc

    if data is None:
        raise ValidationError("document is empty")

    validate_document(data)
    return _build_graph(data)


def _build_graph(data: dict[str, Any]) -> SystemGraph:
    system_raw = data["system"]
    assert isinstance(system_raw, dict)
    description = system_raw.get("description")
    graph = SystemGraph(
        SystemInfo(
            name=str(system_raw["name"]),
            description=str(description) if description is not None else None,
        ),
    )

    nodes = data["nodes"]
    assert isinstance(nodes, list)
    for item in nodes:
        assert isinstance(item, dict)
        graph.add_node(
            Node(
                id=str(item["id"]),
                label=str(item["label"]),
                fillcolor=_node_fillcolor(item),
            ),
        )

    edges = data["edges"]
    assert isinstance(edges, list)
    for item in edges:
        assert isinstance(item, dict)
        graph.add_edge(
            Edge(
                source=str(item["from"]),
                target=str(item["to"]),
                relation=Relation(str(item["relation"])),
            ),
        )

    return graph


def _node_fillcolor(item: dict[str, Any]) -> str | None:
    style = item.get("style")
    if not isinstance(style, dict):
        return None
    fillcolor = style.get("fillcolor")
    return str(fillcolor) if fillcolor is not None else None
