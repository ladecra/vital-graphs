from __future__ import annotations

from pathlib import Path

from vital_graphs.models.system_graph import SystemGraph
from vital_graphs.renderers.mermaid_renderer import render_mermaid

_MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"


def render_html(graph: SystemGraph, output_path: Path) -> None:
    """Write a static HTML file with an embedded Mermaid diagram (no server)."""
    diagram = render_mermaid(graph)
    title = graph.system.name
    description = graph.system.description or ""
    desc_block = f"<p>{_escape(description)}</p>" if description else ""

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape(title)}</title>
  <script src="{_MERMAID_CDN}"></script>
  <style>
    body {{ font-family: Helvetica, Arial, sans-serif; margin: 2rem; max-width: 960px; }}
    h1 {{ font-size: 1.25rem; }}
    p {{ color: #444; }}
  </style>
</head>
<body>
  <h1>{_escape(title)}</h1>
  {desc_block}
  <pre class="mermaid">{diagram}</pre>
  <script>mermaid.initialize({{ startOnLoad: true, securityLevel: "strict" }});</script>
</body>
</html>
"""
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
