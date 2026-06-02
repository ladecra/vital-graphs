# Getting started

## Requirements

- Python 3.12 or newer
- **Graphviz** (the `dot` program on your PATH) — required only for **SVG** and **PNG** export
- Mermaid and HTML export do not use Graphviz

Install Graphviz from [graphviz.org/download](https://graphviz.org/download/).

## Install

```bash
pip install vital-graphs
# or from a clone:
pip install -e ".[dev]"
```

## Validate and render

```bash
vital-graphs validate examples/hpa-axis.yaml
vital-graphs render examples/hpa-axis.yaml -o hpa.svg
vital-graphs render examples/hpa-axis.yaml -o hpa.png
vital-graphs render examples/hpa-axis.yaml -f mermaid -o hpa.mmd
vital-graphs render examples/hpa-axis.yaml -o hpa.html
```

## Python API

```python
from vital_graphs import load, validate, render

graph = load("examples/hpa-axis.yaml")
validate(graph)
render(graph, "hpa.svg")
render(graph, "hpa.mmd", format="mermaid")
```

## Schema

Authoring rules and field reference: [schema.md](schema.md).
