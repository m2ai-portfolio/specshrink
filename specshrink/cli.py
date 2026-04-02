"""Click CLI entry point and command definitions."""

import os
import click
from rich.console import Console
from specshrink.parser import parse_spec, parse_spec_detailed
from specshrink.scorer import score_spec
from specshrink.suggester import suggest_cuts


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


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def score(file):
    """Score a specification file and display complexity verdict."""
    try:
        # Get threshold from environment variable, default to 5
        threshold = int(os.environ.get('SPECSHRINK_THRESHOLD', '5'))

        # Parse the specification with detailed items
        parsed_spec = parse_spec_detailed(file)

        # Score the specification
        scored_metrics = score_spec(parsed_spec.metrics, threshold)

        # Update the parsed_spec with scored metrics
        parsed_spec.metrics = scored_metrics

        # Display the results
        console.print(f"Estimated iterations: {scored_metrics.estimated_iterations}")

        if scored_metrics.within_limit:
            console.print(f"Verdict: PASS (≤{threshold})")
        else:
            console.print(f"Verdict: FAIL (>{threshold})")

            # Display suggestions when FAIL
            suggestions = suggest_cuts(parsed_spec, threshold)
            if suggestions:
                console.print("Suggestions:")
                for suggestion in suggestions:
                    console.print(f"- {suggestion}")

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold red")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold red")
        raise click.Abort()


if __name__ == "__main__":
    cli()
