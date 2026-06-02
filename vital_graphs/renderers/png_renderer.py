from __future__ import annotations

from pathlib import Path

from vital_graphs.models.system_graph import SystemGraph
from vital_graphs.renderers.graphviz_io import render_graphviz


def render_png(graph: SystemGraph, output_path: Path) -> None:
    render_graphviz(graph, output_path, output_format="png")
