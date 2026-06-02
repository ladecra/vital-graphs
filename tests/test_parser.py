from __future__ import annotations

from pathlib import Path

import pytest

from vital_graphs.errors import ValidationError
from vital_graphs.parser import load


def test_load_hpa(hpa_path: Path) -> None:
    graph = load(hpa_path)
    assert graph.system.name == "HPA Axis"
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 3
    assert graph.get_node("crh").label == "CRH"


def test_missing_file() -> None:
    with pytest.raises(ValidationError, match="file not found"):
        load("does-not-exist.yaml")


def test_bad_schema_version(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        'schema_version: "2"\nsystem:\n  name: X\nnodes:\n  - id: a\n    label: A\n'
        "edges:\n  - from: a\n    to: a\n    relation: stimulates\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="schema_version"):
        load(path)


def test_invalid_node_color(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        'schema_version: "1"\nsystem:\n  name: X\nnodes:\n  - id: a\n    label: A\n'
        "    style:\n      fillcolor: blue\nedges:\n  - from: a\n    to: a\n"
        "    relation: stimulates\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="fillcolor"):
        load(path)


def test_unknown_relation(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        'schema_version: "1"\nsystem:\n  name: X\nnodes:\n  - id: a\n    label: A\n'
        "  - id: b\n    label: B\nedges:\n  - from: a\n    to: b\n    relation: causes\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="relation"):
        load(path)
