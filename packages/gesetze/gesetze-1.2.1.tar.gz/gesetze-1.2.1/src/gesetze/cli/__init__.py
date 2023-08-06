"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

import json
from pathlib import Path
from shutil import rmtree

import click

from ..lib.helpers import analyze as analyze_norm
from .factory import Factory


@click.group()
@click.pass_context
@click.option("-v", "--verbose", count=True, help="Enable verbose mode.")
@click.version_option("1.2.1")
def cli(ctx, verbose: int) -> None:
    """
    Utilities for indexing & analyzing german legal norms
    """

    # Ensure context object exists & is dictionary
    ctx.ensure_object(dict)

    # Initialize context object & assign verbose mode
    # IDEA: Implement logger matching verbosity level
    ctx.obj = {"verbose": verbose}


@cli.command()
@click.option("-p", "--providers", multiple=True, help="Provider for legal norms")
@click.option("-d", "--directory", type=click.Path(), help="Output data directory")
@click.option("-m", "--maximum", default=4, help="Maximum for simultaneous requests")
def scrape(providers: tuple, directory: str, maximum: int) -> None:
    """
    Scrapes legal norms from PROVIDER
    """

    # Set fallback
    if not providers:
        providers = [
            # (1) 'gesetze-im-internet.de'
            "gesetze",
            # (2) 'dejure.org'
            "dejure",
            # (3) 'buzer.de'
            "buzer",
            # (4) 'lexparency.de'
            "lexparency",
        ]

    # Loop over providers
    for provider in providers:
        # Define data directory
        data_dir = Path(click.get_app_dir("gesetze"), provider)

        # Initialize scraper
        obj = Factory.create(provider, data_dir)

        # Scrape their data & format it
        data = {item["law"].lower(): item for item in obj.scrape(maximum)}

        # Define data file
        data_file = Path(directory or Path.cwd()) / f"{provider}.json"

        with data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)


@cli.command()
@click.pass_context
def clear(ctx) -> None:
    """
    Clears download cache
    """

    if ctx.obj["verbose"] > 0:
        click.echo("Clearing cache ..", nl=False)

    rmtree(click.get_app_dir("gesetze"))

    if ctx.obj["verbose"] > 0:
        click.echo(" done.")


@cli.command()
@click.pass_context
@click.argument("norm", type=str, nargs=-1)
def analyze(ctx, norm) -> None:
    """
    Analyzes legal NORM
    """

    if ctx.obj["verbose"] > 0:
        click.echo("Analyzing input ..", nl=False)

    result = analyze_norm(" ".join(norm))

    if ctx.obj["verbose"] > 0:
        click.echo(" done.")

    for key, value in result.items():
        click.echo(f"{key.capitalize()}: {value}")
