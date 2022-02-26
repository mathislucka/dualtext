import click
import keyring

from session import Session
from settings import API_URL
from cli_project import project
from cli_corpus import corpus

@click.group()
@click.pass_context
def cli(ctx):
    pass


cli.add_command(project)
cli.add_command(corpus)





