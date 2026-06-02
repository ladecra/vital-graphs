# AGENTS.md

## Project

Vital Graphs

Vital Graphs is a lightweight open-source Python library that converts human-readable biological system descriptions into publication-quality systems diagrams.

The project exists to make causal architecture visible.

Users describe nodes and relationships in YAML.

Vital Graphs produces:

* SVG diagrams
* PNG diagrams
* Mermaid diagrams
* Interactive HTML graphs

The project is intentionally focused on visualization, not simulation.

---

## Core Philosophy

A biological system is a graph before it is a model.

The purpose of Vital Graphs is to make feedback loops, signaling relationships, dependencies, constraints, and causal structure legible.

The project favors:

* Clarity over complexity
* Explicit structure over inference
* Human readability over compact syntax
* Stability over feature growth

---

## Non-Goals

Vital Graphs is NOT:

* a physiology simulator
* a systems biology engine
* a machine learning platform
* an agent framework
* a database
* a knowledge graph platform
* an AI assistant

Do not introduce functionality that moves the project toward those domains.

---

## Design Constraints

All user-authored files should remain human-readable.

A biology student should be able to understand a graph definition without programming knowledge.

Prefer YAML over custom DSLs.

Prefer explicit declarations over implicit behavior.

Avoid configuration sprawl.

---

## Version 1 Success Criteria

A user can:

1. Write a biological system in YAML.
2. Validate the file.
3. Generate a diagram.
4. Export the diagram.

The entire workflow should take less than one minute.

If a feature does not support this workflow, it should not be added to Version 1.

---

## Technical Debt Awareness

Avoid introducing:

* plugin systems
* web servers
* cloud integrations
* databases
* authentication
* distributed architecture
* simulation engines

These may become future projects but are outside the scope of Vital Graphs.

If a proposed implementation adds substantial complexity without directly improving graph creation or export, reject it.

---

## Preferred Technologies

Python 3.12+

Core dependencies:

* networkx
* pyyaml
* typer
* graphviz

Optional dependencies:

* matplotlib
* pygraphviz

Keep dependency count low.

---

## Repository Standards

All code should be:

* typed
* tested
* documented

Public APIs should remain stable whenever possible.

Favor simple modules under 300 lines.

Avoid large monolithic files.

---

## Architectural Principle

The parser should know nothing about rendering.

The renderer should know nothing about YAML.

The graph model is the boundary between them.

Maintain strict separation between:

Input → Graph Model → Output

This separation is a project invariant.
