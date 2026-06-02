from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from vital_graphs import load, render, validate
from vital_graphs.errors import ValidationError
from vital_graphs.render import OutputFormat, resolve_format
from vital_graphs.renderers.graphviz_io import require_graphviz
from vital_graphs.renderers.mermaid_renderer import render_mermaid

pytestmark_graphviz = pytest.mark.skipif(
    shutil.which("dot") is None,
    reason="Graphviz dot not installed",
)

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_resolve_format_from_suffix() -> None:
    assert resolve_format(Path("out.svg")) == OutputFormat.SVG
    assert resolve_format(Path("out.mmd")) == OutputFormat.MERMAID


def test_mermaid_content(hpa_path: Path) -> None:
    graph = load(hpa_path)
    text = render_mermaid(graph)
    assert "flowchart LR" in text
    assert "crh" in text
    assert "stimulates" in text
    assert "inhibits" in text


def test_render_mermaid_file(hpa_path: Path, tmp_path: Path) -> None:
    graph = load(hpa_path)
    out = tmp_path / "hpa.mmd"
    render(graph, out)
    assert "inhibits" in out.read_text(encoding="utf-8")


def test_render_html_file(hpa_path: Path, tmp_path: Path) -> None:
    graph = load(hpa_path)
    out = tmp_path / "hpa.html"
    render(graph, out)
    body = out.read_text(encoding="utf-8")
    assert "HPA Axis" in body
    assert "mermaid" in body
    assert "crh" in body


def test_graphviz_required_for_svg(hpa_path: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda _: None)
    graph = load(hpa_path)
    with pytest.raises(ValidationError, match="Graphviz"):
        render(graph, tmp_path / "x.svg")


@pytestmark_graphviz
def test_render_hpa_svg(hpa_path: Path, tmp_path: Path) -> None:
    graph = load(hpa_path)
    validate(graph)
    out = tmp_path / "hpa.svg"
    render(graph, out)
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "CRH" in text
    assert "stimulates" in text


@pytestmark_graphviz
@pytest.mark.parametrize(
    "name",
    [
        "hpa-axis.yaml",
        "insulin-regulation.yaml",
        "thyroid-axis.yaml",
        "cortisol.yaml",
    ],
)
def test_all_examples_render_svg(name: str, tmp_path: Path) -> None:
    graph = load(EXAMPLES / name)
    validate(graph)
    out = tmp_path / f"{name}.svg"
    render(graph, out)
    assert out.stat().st_size > 100


@pytestmark_graphviz
def test_render_png(hpa_path: Path, tmp_path: Path) -> None:
    graph = load(hpa_path)
    out = tmp_path / "hpa.png"
    render(graph, out)
    assert out.stat().st_size > 100


def test_require_graphviz_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda _: None)
    with pytest.raises(ValidationError, match="Graphviz"):
        require_graphviz()
