# Architecture

Vital Graphs separates input parsing, validation, the graph model, and rendering.

```
YAML
  ↓
Parser
  ↓
Validator (document structure)
  ↓
SystemGraph (graph integrity)
  ↓
Renderer
  ↓
Output (SVG, PNG, Mermaid, HTML)
```

## Invariants

- **No renderer imports the parser.** Renderers consume `SystemGraph` only.
- **No parser imports renderers.** The parser produces `SystemGraph` only.
- **SystemGraph is the shared abstraction** between layers.
- **NetworkX** may be used inside layout/render utilities; it is not part of the public API.
- **Graphviz** is the sole layout engine for v0.1.

## Module roles

| Module | Role |
|--------|------|
| `parser.py` | Load YAML; delegate structural validation |
| `validators/schema.py` | Required keys, types, relation enum |
| `models/system_graph.py` | Nodes, edges, integrity rules |
| `graph.py` | Internal conversion for layout (not public) |
| `render.py` | Dispatch to format-specific renderers |
| `renderers/svg_renderer.py` | Graphviz → SVG |
| `renderers/png_renderer.py` | Graphviz → PNG |
| `renderers/mermaid_renderer.py` | Mermaid flowchart text |
| `renderers/html_renderer.py` | Static HTML + Mermaid.js CDN |
| `cli.py` | `validate` and `render` commands |

## Validation split

**Parser / schema validator**

- YAML syntax (via PyYAML)
- Required fields and types
- `schema_version`, relation enum

**SystemGraph**

- Unique node ids
- Edge endpoints reference existing nodes
- No duplicate edges
