"""Click CLI entry point and command definitions."""

import click
from rich.console import Console
from specshrink.parser import parse_spec


console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="specshrink")
def cli():
    """SpecShrink - Analyze app specifications and recommend scope cuts."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def parse(file):
    """Parse a specification file and display basic metrics."""
    try:
        metrics = parse_spec(file)

        # Display the metrics
        console.print(f"Features: {metrics.features}")
        console.print(f"External deps: {metrics.external_deps}")
        console.print(f"Integration points: {metrics.integration_points}")

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold red")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold red")
        raise click.Abort()


if __name__ == "__main__":
    cli()
