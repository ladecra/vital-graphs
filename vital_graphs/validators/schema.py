from __future__ import annotations

import re

from vital_graphs.errors import ValidationError
from vital_graphs.models.edge import Relation
from vital_graphs.models.system_graph import SystemGraph

_HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")

SCHEMA_VERSION = "1"
ALLOWED_RELATIONS = {r.value for r in Relation}


def validate_document(data: object) -> None:
    """Validate parsed YAML structure before building a SystemGraph."""
    if not isinstance(data, dict):
        raise ValidationError("root must be a mapping")

    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise ValidationError(
            f'schema_version must be "{SCHEMA_VERSION}"',
            path="schema_version",
        )

    system = data.get("system")
    if not isinstance(system, dict):
        raise ValidationError("system must be a mapping", path="system")
    name = system.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("system.name must be a non-empty string", path="system.name")
    description = system.get("description")
    if description is not None and not isinstance(description, str):
        raise ValidationError("system.description must be a string", path="system.description")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or len(nodes) == 0:
        raise ValidationError("nodes must be a non-empty list", path="nodes")

    seen_ids: set[str] = set()
    for index, item in enumerate(nodes):
        path = f"nodes[{index}]"
        if not isinstance(item, dict):
            raise ValidationError("node must be a mapping", path=path)
        node_id = item.get("id")
        label = item.get("label")
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValidationError("node id must be a non-empty string", path=f"{path}.id")
        if not isinstance(label, str) or not label.strip():
            raise ValidationError("node label must be a non-empty string", path=f"{path}.label")
        if node_id in seen_ids:
            raise ValidationError(f"duplicate node id in document: {node_id!r}", path=f"{path}.id")
        seen_ids.add(node_id)
        _validate_node_style(item, path)

    edges = data.get("edges")
    if not isinstance(edges, list) or len(edges) == 0:
        raise ValidationError("edges must be a non-empty list", path="edges")

    for index, item in enumerate(edges):
        path = f"edges[{index}]"
        if not isinstance(item, dict):
            raise ValidationError("edge must be a mapping", path=path)
        source = item.get("from")
        target = item.get("to")
        relation = item.get("relation")
        if not isinstance(source, str) or not source.strip():
            raise ValidationError("edge from must be a non-empty string", path=f"{path}.from")
        if not isinstance(target, str) or not target.strip():
            raise ValidationError("edge to must be a non-empty string", path=f"{path}.to")
        if source not in seen_ids:
            raise ValidationError(f"unknown node id: {source!r}", path=f"{path}.from")
        if target not in seen_ids:
            raise ValidationError(f"unknown node id: {target!r}", path=f"{path}.to")
        if not isinstance(relation, str) or relation not in ALLOWED_RELATIONS:
            raise ValidationError(
                f"relation must be one of: {', '.join(sorted(ALLOWED_RELATIONS))}",
                path=f"{path}.relation",
            )


def validate(graph: SystemGraph) -> None:
    """Validate graph integrity (public API)."""
    validate_graph(graph)


def validate_graph(graph: SystemGraph) -> None:
    graph.validate_integrity()


def _validate_node_style(item: dict[str, object], path: str) -> None:
    style = item.get("style")
    if style is None:
        return
    if not isinstance(style, dict):
        raise ValidationError("node style must be a mapping", path=f"{path}.style")
    fillcolor = style.get("fillcolor")
    if fillcolor is None:
        return
    if not isinstance(fillcolor, str) or not _HEX_COLOR.match(fillcolor):
        raise ValidationError(
            "style.fillcolor must be a hex color like #aabbcc",
            path=f"{path}.style.fillcolor",
        )
