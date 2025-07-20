# cli/main.py
import json
import click
import requests
from pathlib import Path

API_BASE = "http://localhost:8000/networks"


@click.group()
def cli():
    """Bayes CLI – manage Bayesian networks via REST API."""
    pass


@cli.command()
@click.argument("name")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def upload(name, file):
    """Upload a Bayesian Network from FILE and save it as NAME."""
    data = json.loads(file.read_text())
    response = requests.post(f"{API_BASE}/{name}", json=data)
    click.echo(response.json())


@cli.command()
@click.argument("name")
def get(name):
    """Get a Bayesian Network by NAME."""
    response = requests.get(f"{API_BASE}/{name}")
    if response.status_code == 404:
        click.echo(f"❌ Network '{name}' not found.")
    else:
        click.echo(json.dumps(response.json(), indent=2))


@cli.command(name="list")
def list_networks():
    """List all stored Bayesian Networks."""
    response = requests.get(API_BASE)
    click.echo(response.json())


if __name__ == "__main__":
    cli()
