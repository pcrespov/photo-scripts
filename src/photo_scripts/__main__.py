import click
from . import delete_duplicates
from . import delete_empty_folders



@click.command()
def cli():
    """ Minimal """
    click.echo("Hoi there")


