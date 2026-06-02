from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from vital_graphs import load, render, validate
from vital_graphs.errors import ValidationError
from vital_graphs.render import OutputFormat

app = typer.Typer(
    name="vital-graphs",
    help="Validate and render biological system graphs from YAML.",
    no_args_is_help=True,
)

_FORMAT_HELP = "Output format: svg, png, mermaid, html (default: infer from -o extension)"


def _default_output(file: Path, fmt: OutputFormat) -> Path:
    suffix = {
        OutputFormat.SVG: ".svg",
        OutputFormat.PNG: ".png",
        OutputFormat.MERMAID: ".mmd",
        OutputFormat.HTML: ".html",
    }[fmt]
    return file.with_suffix(suffix)


@app.command("validate")
def validate_cmd(
    file: Annotated[Path, typer.Argument(help="YAML system definition")],
) -> None:
    """Validate a YAML file without rendering."""
    try:
        graph = load(file)
        validate(graph)
    except ValidationError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"OK: {file}")


@app.command("render")
def render_cmd(
    file: Annotated[Path, typer.Argument(help="YAML system definition")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output file path"),
    ] = None,
    format: Annotated[
        str | None,
        typer.Option("--format", "-f", help=_FORMAT_HELP),
    ] = None,
) -> None:
    """Render a YAML file to SVG, PNG, Mermaid, or HTML."""
    try:
        graph = load(file)
        validate(graph)
        if output is None and format is None:
            out = file.with_suffix(".svg")
            result = render(graph, out)
        elif output is None:
            assert format is not None
            fmt = OutputFormat(format.lower().lstrip("."))
            out = _default_output(file, fmt)
            result = render(graph, out, format=format)
        else:
            result = render(graph, output, format=format)
    except ValidationError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"Wrote {result}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
