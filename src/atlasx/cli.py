"""Command-line interface for AtlasX."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from atlasx.io.loaders import create_minimal_project
from atlasx.lifecycle import regenerate_graph, regenerate_report, run_pipeline
from atlasx.utils.logging import console

app = typer.Typer(
    name="atlasx",
    help="AtlasX Discovery Layer: first-principles research sensemaking.",
    no_args_is_help=True,
)


@app.command("init")
def init_project(
    project: Annotated[
        Path,
        typer.Option("--project", "-p", help="Project directory to create."),
    ] = Path("."),
) -> None:
    """Create a minimal AtlasX project folder."""

    create_minimal_project(project)
    console.print(f"[green]Initialized AtlasX project at[/green] {project.resolve()}")


@app.command("run")
def run_command(
    project: Annotated[
        Path,
        typer.Option("--project", "-p", help="AtlasX project directory."),
    ],
    provider: Annotated[
        str,
        typer.Option("--provider", help="Provider: offline, local, or openai."),
    ] = "offline",
    model: Annotated[
        str | None,
        typer.Option("--model", help="Model name for OpenAI or local provider."),
    ] = None,
) -> None:
    """Run the full AtlasX pipeline."""

    result = run_pipeline(project=project, provider_name=provider, model=model)
    table = Table(title="AtlasX run complete")
    table.add_column("Metric")
    table.add_column("Value")
    for key, value in result.items():
        table.add_row(str(key), str(value))
    console.print(table)


@app.command("graph")
def graph_command(
    project: Annotated[
        Path,
        typer.Option("--project", "-p", help="AtlasX project directory."),
    ],
) -> None:
    """Regenerate graph CSV files from existing extractions."""

    result = regenerate_graph(project)
    console.print(f"[green]Graph written:[/green] {result}")


@app.command("report")
def report_command(
    project: Annotated[
        Path,
        typer.Option("--project", "-p", help="AtlasX project directory."),
    ],
) -> None:
    """Regenerate Markdown reports from existing extractions."""

    result = regenerate_report(project)
    console.print(f"[green]Reports written:[/green] {result}")


if __name__ == "__main__":
    app()

