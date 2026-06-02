# Changelog

## 1.0.0

- Stable YAML schema v1 with `schema_version: "1"`
- Validate and render CLI (`validate`, `render` with `-o` and `-f`)
- Public API: `load`, `validate`, `render`, `OutputFormat`
- Export formats: SVG, PNG (Graphviz), Mermaid, static HTML (Mermaid.js CDN)
- Optional per-node `style.fillcolor` for Graphviz outputs
- Example library and template under `examples/`

## 0.1.0

- Initial release: YAML parsing, validation, Graphviz SVG export
