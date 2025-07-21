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

@cli.command()
@click.argument("name")
@click.option("--evidence", help="JSON dict of evidence", required=True)
@click.option("--iterations", default=10)
def infer(name, evidence, iterations):
    parsed = json.loads(evidence)
    response = requests.post(f"{API_BASE}/{name}/infer", json={"evidence": parsed, "iterations": iterations})
    click.echo(json.dumps(response.json(), indent=2))

@cli.command()
@click.argument("name")
def graph(name):
    """Print the graph structure of a Bayesian Network."""
    response = requests.get(f"{API_BASE}/{name}/graph")
    if response.status_code == 404:
        click.echo(f"❌ Network '{name}' not found.")
    else:
        click.echo(json.dumps(response.json(), indent=2))
