# YAML schema (v1)

The YAML schema is a stable public interface beginning with v0.1.0. Prefer additive changes over breaking changes.

## Root

| Field | Required | Description |
|-------|----------|-------------|
| `schema_version` | yes | Must be `"1"` |
| `system` | yes | Metadata for the diagram |
| `nodes` | yes | List of nodes |
| `edges` | yes | List of directed relationships |

## `system`

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Human-readable system title (shown in diagram title when supported) |
| `description` | no | Optional short context |

## `nodes`

Each item:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Machine identifier (used in `edges`); stable, unique |
| `label` | yes | Text shown on the diagram |
| `style` | no | Optional presentation (Graphviz SVG/PNG only) |

### Optional `style` (nodes)

| Field | Description |
|-------|-------------|
| `fillcolor` | Hex fill color for the node box, e.g. `#d6eaf8` |

Node `id` values are canonical graph identifiers. Renderers display `label`, not `id`.

## `edges`

Each item:

| Field | Required | Description |
|-------|----------|-------------|
| `from` | yes | Source node `id` |
| `to` | yes | Target node `id` |
| `relation` | yes | One of: `stimulates`, `inhibits`, `regulates`, `depends_on` |

Duplicate edges with the same `(from, to, relation)` are not allowed.

## Example

```yaml
schema_version: "1"

system:
  name: HPA Axis

nodes:
  - id: crh
    label: CRH
  - id: acth
    label: ACTH
  - id: cortisol
    label: Cortisol

edges:
  - from: crh
    to: acth
    relation: stimulates
  - from: acth
    to: cortisol
    relation: stimulates
  - from: cortisol
    to: crh
    relation: inhibits
```

## Future evolution

A later version may add optional `label` on edges for display while keeping `relation` as the semantic enum.
