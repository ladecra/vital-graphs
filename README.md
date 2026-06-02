# vital-graphs

# Vital Graphs

Convert human-readable biological system descriptions in YAML into systems diagrams.

## Install

```bash
pip install -e ".[dev]"
```

**Graphviz** is required on the machine where you run **SVG** or **PNG** export (`dot` on your PATH). Install from [graphviz.org/download](https://graphviz.org/download/). Mermaid (`.mmd`) and HTML export do not need Graphviz.

## Quick start

```bash
vital-graphs validate examples/hpa-axis.yaml
vital-graphs render examples/hpa-axis.yaml -o hpa.svg
vital-graphs render examples/hpa-axis.yaml -f mermaid -o hpa.mmd
vital-graphs render examples/hpa-axis.yaml -o hpa.html
```

## Python API

```python
from vital_graphs import load, validate, render

graph = load("examples/hpa-axis.yaml")
validate(graph)
render(graph, "hpa.svg")
```

## Documentation

- [Getting started](docs/getting-started.md)
- [YAML schema](docs/schema.md)
- [Architecture](docs/architecture.md)
- [Examples](docs/examples.md)

## License

MIT
