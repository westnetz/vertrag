import click
import os
import sys

from pprint import pprint
from .initialize import init_dir, check_dir, VertragCheckError
from .contract import ContractFactory, render_contract, send_contract
from .config import get_config

cwd = os.getcwd()
try:
    config = get_config(cwd)
    cf = ContractFactory(config, cwd)
    initialized=True
except FileNotFoundError:
    initialized=False

def exit_if_config_not_found():
    if not initialized:
        print("No config found. Did you forget to initialize here with 'vertrag init'?")
        sys.exit(1)

@click.group()
def cli1():
    """
    vertrag command line interface.
    """
    pass


@cli1.command()
@click.option(
    "--without-samples",
    is_flag=True,
    help="Create working directory without sample customers",
    default=False
)
def init(without_samples):
    """
    Create the directory structure in the current directory.
    """
    print("Initializing...")

    try:
        init_dir(cwd, without_samples)
    except Exception as e:
        print("Failed. :/")
        sys.exit(1)

    print("Finished.")

@cli1.command()
def check():
    """
    Check the directory structure in the current working directory.
    """
    try:
        check_dir(cwd)
    except VertragCheckError as e:
        print(e)
        sys.exit(1)

@cli1.command()
@click.argument("anschluss_order_id")
def create(anschluss_order_id):
    """
    Create a contract.
    """
    exit_if_config_not_found()
    print("Creating contract...")
    c = cf.from_order(anschluss_order_id)
    pprint(c._data)
    c.to_yaml()


@cli1.command()
@click.argument("contract_id")
def render(contract_id):
    """
    Render a contract to pdf.
    """
    exit_if_config_not_found()
    print("Rendering contract...")
    c = cf.from_contract(contract_id)
    c.to_pdf()


@cli1.command()
@click.argument("contract_id")
def send(contract_id):
    """
    Send contract by email.
    """
    exit_if_config_not_found()
    print("Sending contract *.{}".format(contract_id))
    c = cf.from_contract(contract_id)
    c.send()


cli = click.CommandCollection(sources=[cli1])

if __name__ == "__main__":
    cli()
