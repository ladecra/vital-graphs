# index.md

## Repository Structure

vital-graphs/

README.md
LICENSE
AGENTS.md
ROADMAP.md
index.md
pyproject.toml

docs/

```
getting-started.md
architecture.md
examples.md
```

examples/

```
cortisol.yaml
hpa-axis.yaml
insulin-regulation.yaml
thyroid-axis.yaml
```

tests/

```
test_parser.py
test_graph.py
test_render.py
test_cli.py
```

vital_graphs/

```
__init__.py

parser.py
graph.py
render.py
cli.py

models/

    node.py
    edge.py
    system_graph.py

renderers/

    svg_renderer.py
    mermaid_renderer.py
    html_renderer.py

validators/

    schema.py
```

---

## Data Flow

YAML
↓

Parser

↓

System Graph

↓

Renderer

↓

SVG / PNG / Mermaid / HTML

---

## Module Responsibilities

parser.py

Convert YAML into graph objects.

Must contain no rendering logic.

---

graph.py

Internal graph construction.

Owns graph relationships.

Must contain no export logic.

---

render.py

Dispatch layer.

Routes graph objects to renderers.

---

renderers/

Output generation only.

Must not parse YAML.

---

validators/

Input validation.

Must not modify graph structure.

---

## Architectural Invariants

No renderer may import parser modules.

No parser may import renderer modules.

Graph objects are the only shared abstraction.

All outputs must derive from the graph model.
