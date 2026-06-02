from __future__ import annotations

import shutil
from pathlib import Path

from vital_graphs.errors import ValidationError
from vital_graphs.models.system_graph import SystemGraph
from vital_graphs.renderers.graphviz_builder import build_digraph


def require_graphviz() -> None:
    if shutil.which("dot") is None:
        raise ValidationError(
            "Graphviz is required for SVG and PNG export. "
            "Install the Graphviz package and ensure the `dot` command is on your PATH. "
            "See https://graphviz.org/download/",
        )


def render_graphviz(
    graph: SystemGraph,
    output_path: Path,
    *,
    output_format: str,
) -> None:
    """Write SVG or PNG via Graphviz."""
    require_graphviz()
    dot = build_digraph(graph, output_format=output_format)
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stem = output_path.with_suffix("")
    dot.render(filename=str(stem), cleanup=True)
    rendered = stem.with_suffix(f".{output_format}")
    if rendered != output_path and rendered.exists():
        rendered.replace(output_path)
