The implementation plan is approved with the following modifications and clarifications.

# Architectural Clarifications

## 1. Schema Is Part of the Public API

The YAML schema is now a first-class public interface.

Create:

docs/schema.md

The schema should be considered stable beginning with v0.1.0.

Future changes should prefer additive evolution over breaking changes.

Add:

schema_version: "1"

to the root level immediately.

Example:

schema_version: "1"

system:
name: HPA Axis

nodes:

* id: crh
  label: CRH

edges:

* from: crh
  to: acth
  relation: stimulates

This costs almost nothing today and prevents migration problems later.

---

## 2. Node IDs Are Canonical

Node ids are machine identifiers.

Labels are presentation.

Example:

* id: corticotropin_releasing_hormone
  label: CRH

Renderers should display labels.

Graph relationships should use ids.

Never use labels as graph identifiers.

---

## 3. Edge Semantics

For v0.1 use a closed enum.

Allowed relations:

stimulates
inhibits
regulates
depends_on

No free-text relationships in v0.1.

Reason:

Graph styling, validation, Mermaid export, and future consistency all become dramatically simpler.

A future version may allow:

label: custom text

while preserving the underlying relation enum.

Example:

relation: stimulates
label: promotes

The semantic relationship remains stable.

---

## 4. SystemGraph Owns Validation Invariants

Parser validates file structure.

SystemGraph validates graph integrity.

Example:

Parser responsibility:

* YAML syntax
* required keys
* field types

SystemGraph responsibility:

* unique node ids
* dangling references
* duplicate edges

Keep these concerns separate.

---

## 5. NetworkX Is Infrastructure, Not Domain

SystemGraph is the authoritative graph representation.

NetworkX is an implementation detail.

Do not expose NetworkX types through the public API.

Avoid:

load_yaml() -> nx.DiGraph

Prefer:

load_yaml() -> SystemGraph

Renderer and graph utilities may internally convert to NetworkX.

This preserves future flexibility.

---

## 6. Graphviz Is The Sole Layout Engine For v0.1

Lock this decision.

Do not introduce alternative layout engines.

Do not expose layout configuration yet.

The project goal is:

correct diagram generation

not

layout customization

One rendering path means fewer variables and faster stabilization.

---

# Repository Additions

Add:

docs/schema.md
docs/architecture.md

Architecture documentation should include:

YAML
↓

Parser

↓

Validator

↓

SystemGraph

↓

Renderer

↓

Output

The parser-to-graph-model-to-renderer separation is a project invariant.

---

# Public Python API

Target API:

from vital_graphs import load, validate, render

graph = load("hpa-axis.yaml")

validate(graph)

render(graph, "out.svg")

Keep the API intentionally tiny.

Anything larger than this should be justified.

---

# CLI Contract

The CLI is part of the public API.

Lock commands early:

vital-graphs validate file.yaml

vital-graphs render file.yaml

vital-graphs render file.yaml -o output.svg

Future versions may add:

--format mermaid
--format png
--format html

Avoid redesigning CLI semantics after release.

---

# Testing Philosophy

Do not test Graphviz output pixels.

Test:

* parser correctness
* validation correctness
* graph construction
* renderer invocation

Renderer smoke tests should assert:

* output file created
* SVG contains expected labels
* SVG contains expected edge labels

Avoid fragile snapshot tests.

---

# Example Library

Treat examples as product assets.

Initial examples:

examples/hpa-axis.yaml
examples/insulin-regulation.yaml
examples/thyroid-axis.yaml

Each example should render successfully in CI.

Examples are executable documentation.

---

# Deferred Features

Explicitly reject for v0.1:

* simulation
* differential equations
* biological ontologies
* AI generation
* graph editing UI
* databases
* plugins
* web servers
* pathway inference

If implementation begins drifting toward any of these areas, stop and reassess.

---

# Definition Of Done For v0.1

A new user can:

1. Install the package.

2. Open an example YAML file.

3. Run:

   vital-graphs validate examples/hpa-axis.yaml

4. Run:

   vital-graphs render examples/hpa-axis.yaml -o hpa.svg

5. Open a correctly labeled SVG diagram.

If this workflow succeeds in under one minute, v0.1 is complete.

Begin implementation using the critical path:

schema.md
models/
validator
parser
SVG renderer
render.py
CLI
examples
README

Do not implement Mermaid, PNG, or HTML until SVG is stable.
