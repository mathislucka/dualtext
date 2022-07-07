import click
import keyring

from session import Session
from settings import API_URL
from cli_project import project
from cli_corpus import corpus
from cli_label import label
from settings import API_URL, set_config, get_config

@click.group()
@click.pass_context
def cli(ctx):
    if not API_URL and not ctx.invoked_subcommand == 'setconfig' and not ctx.invoked_subcommand == 'getconfig':
        click.secho("You have not configured your API endpoint. Please configure your endpoint:\n", fg='red', bold=True, err=True)
        click.echo("dualtext setconfig --api-endpoint <your-host> \n", err=True)
        ctx.abort()
    
    click.secho(f'Using {API_URL}...\n', fg="green", bold=True, err=True)

@cli.command('setconfig')
@click.option('--api-endpoint', type=str, help='The API endpoint where your dualtext instance is running ( https://<hostname> ).')
def set_dualtext_config(api_endpoint):
    set_config(API_URL=api_endpoint)



@cli.command('getconfig')
def get_dualtext_config():
    click.echo(get_config())


cli.add_command(project)
cli.add_command(corpus)
cli.add_command(label)
