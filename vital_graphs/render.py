from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from vital_graphs.errors import ValidationError
from vital_graphs.models.system_graph import SystemGraph
from vital_graphs.renderers.html_renderer import render_html
from vital_graphs.renderers.mermaid_renderer import render_mermaid
from vital_graphs.renderers.png_renderer import render_png
from vital_graphs.renderers.svg_renderer import render_svg


class OutputFormat(StrEnum):
    SVG = "svg"
    PNG = "png"
    MERMAID = "mermaid"
    HTML = "html"


_SUFFIX_FORMAT: dict[str, OutputFormat] = {
    ".svg": OutputFormat.SVG,
    ".png": OutputFormat.PNG,
    ".mmd": OutputFormat.MERMAID,
    ".mermaid": OutputFormat.MERMAID,
    ".html": OutputFormat.HTML,
    ".htm": OutputFormat.HTML,
}


def resolve_format(path: Path, format_name: str | None = None) -> OutputFormat:
    if format_name is not None:
        try:
            return OutputFormat(format_name.lower().lstrip("."))
        except ValueError as exc:
            allowed = ", ".join(f.value for f in OutputFormat)
            raise ValidationError(
                f"unknown format {format_name!r}; use one of: {allowed}",
            ) from exc
    suffix = path.suffix.lower()
    if suffix not in _SUFFIX_FORMAT:
        raise ValidationError(
            f"cannot infer output format from {path.suffix!r}; "
            "use a supported extension or pass format=",
        )
    return _SUFFIX_FORMAT[suffix]


def render(
    graph: SystemGraph,
    output: str | Path,
    *,
    format: str | None = None,
) -> Path:
    """Render a SystemGraph to a file. Format is inferred from the path or format=."""
    path = Path(output)
    fmt = resolve_format(path, format)

    if fmt == OutputFormat.SVG:
        render_svg(graph, path)
    elif fmt == OutputFormat.PNG:
        render_png(graph, path)
    elif fmt == OutputFormat.MERMAID:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_mermaid(graph), encoding="utf-8")
    elif fmt == OutputFormat.HTML:
        render_html(graph, path)
    else:
        raise ValidationError(f"unsupported format: {fmt}")

    if not path.is_file():
        raise ValidationError(f"render failed: {path} was not created")
    return path
