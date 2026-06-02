# Examples

Runnable graphs live in `examples/`. Each file validates and renders in CI.

| File | Topic |
|------|--------|
| `hpa-axis.yaml` | Hypothalamic-pituitary-adrenal axis with cortisol feedback |
| `insulin-regulation.yaml` | Glucose–insulin homeostasis |
| `thyroid-axis.yaml` | Hypothalamic-pituitary-thyroid axis |
| `cortisol.yaml` | Cortisol signaling with optional node colors |

## Templates

`examples/templates/minimal-feedback-loop.yaml` is a starting point for a two-node feedback loop. Copy it, rename nodes and labels, and extend edges.

## Try all formats

```bash
for f in examples/*.yaml; do
  base="${f%.yaml}"
  vital-graphs render "$f" -o "${base}.svg"
  vital-graphs render "$f" -f mermaid -o "${base}.mmd"
done
```
