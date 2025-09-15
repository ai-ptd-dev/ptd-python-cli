#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import click

from .commands.benchmark import BenchmarkCommand
from .commands.hello import HelloCommand
from .commands.version import VersionCommand
from .utils.logger import Logger


@click.group()
@click.version_option()
def cli() -> None:
    """BasicCli - A Python CLI framework demonstrating PTD"""
    pass


@cli.command()
@click.argument("name")
@click.option("--uppercase", "-u", is_flag=True, help="Print greeting in uppercase")
@click.option("--repeat", "-r", type=int, default=1, help="Repeat the greeting N times")
def hello(name: str, uppercase: bool, repeat: int) -> None:
    """Greet someone with a personalized message"""
    command = HelloCommand(name, uppercase=uppercase, repeat=repeat)
    result = command.execute()
    if not result.success:
        click.echo(f"Error: {result.message}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "output_json", is_flag=True, help="Output version info as JSON")
def version(output_json: bool) -> None:
    """Display version information"""
    command = VersionCommand(output_json=output_json)
    result = command.execute()
    if not result.success:
        click.echo(f"Error: {result.message}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("iterations", type=int, default=1000)
@click.option(
    "--output",
    type=click.Choice(["console", "json", "csv"]),
    default="console",
    help="Output format",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Show detailed benchmark information"
)
def benchmark(iterations: int, output: str, verbose: bool) -> None:
    """Run performance benchmarks"""
    command = BenchmarkCommand(iterations, output_format=output, verbose=verbose)
    result = command.execute()
    if not result.success:
        click.echo(f"Error: {result.message}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--pretty", "-p", is_flag=True, help="Pretty print JSON output")
@click.option("--stats", "-s", is_flag=True, help="Show processing statistics")
def process(file: str, pretty: bool, stats: bool) -> None:
    """Process a JSON file and demonstrate file I/O"""
    logger = Logger(verbose=stats)
    file_path = Path(file)

    try:
        logger.info(f"Processing file: {file}")

        if not file_path.exists():
            logger.error(f"File not found: {file}")
            sys.exit(1)

        content = file_path.read_text()
        data = json.loads(content)

        logger.info(f"Successfully parsed JSON with {len(data.keys())} keys")

        if pretty:
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(json.dumps(data))

        if stats:
            logger.info(f"File size: {file_path.stat().st_size} bytes")
            logger.info("Processing complete")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
