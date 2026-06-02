from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from vital_graphs.cli import app

runner = CliRunner()
needs_dot = pytest.mark.skipif(shutil.which("dot") is None, reason="Graphviz not installed")


def test_validate_ok(hpa_path: Path) -> None:
    result = runner.invoke(app, ["validate", str(hpa_path)])
    assert result.exit_code == 0
    assert "OK" in result.stdout


def test_validate_failure(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("not: valid\n", encoding="utf-8")
    result = runner.invoke(app, ["validate", str(bad)])
    assert result.exit_code == 1


@needs_dot
def test_render_ok(hpa_path: Path, tmp_path: Path) -> None:
    out = tmp_path / "out.svg"
    result = runner.invoke(app, ["render", str(hpa_path), "-o", str(out)])
    assert result.exit_code == 0
    assert out.is_file()


def test_render_mermaid_cli(hpa_path: Path, tmp_path: Path) -> None:
    out = tmp_path / "out.mmd"
    result = runner.invoke(
        app,
        ["render", str(hpa_path), "-f", "mermaid", "-o", str(out)],
    )
    assert result.exit_code == 0
    assert "flowchart" in out.read_text(encoding="utf-8")
