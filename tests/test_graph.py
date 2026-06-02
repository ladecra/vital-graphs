from __future__ import annotations

import pytest

from vital_graphs.errors import GraphIntegrityError
from vital_graphs.models.edge import Edge, Relation
from vital_graphs.models.node import Node
from vital_graphs.models.system_graph import SystemGraph, SystemInfo


def test_add_nodes_and_edges() -> None:
    graph = SystemGraph(SystemInfo(name="test"))
    graph.add_node(Node(id="a", label="A"))
    graph.add_node(Node(id="b", label="B"))
    graph.add_edge(Edge(source="a", target="b", relation=Relation.STIMULATES))
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1


def test_duplicate_node_id() -> None:
    graph = SystemGraph(SystemInfo(name="test"))
    graph.add_node(Node(id="a", label="A"))
    with pytest.raises(GraphIntegrityError, match="duplicate"):
        graph.add_node(Node(id="a", label="A again"))


def test_dangling_edge() -> None:
    graph = SystemGraph(SystemInfo(name="test"))
    graph.add_node(Node(id="a", label="A"))
    with pytest.raises(GraphIntegrityError, match="not a defined node"):
        graph.add_edge(Edge(source="a", target="missing", relation=Relation.INHIBITS))


def test_duplicate_edge() -> None:
    graph = SystemGraph(SystemInfo(name="test"))
    graph.add_node(Node(id="a", label="A"))
    graph.add_node(Node(id="b", label="B"))
    graph.add_edge(Edge(source="a", target="b", relation=Relation.REGULATES))
    with pytest.raises(GraphIntegrityError, match="duplicate edge"):
        graph.add_edge(Edge(source="a", target="b", relation=Relation.REGULATES))
