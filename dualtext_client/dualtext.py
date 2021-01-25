import click
import keyring
import json
import sys
from session import Session
from project import Project

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    access_token = keyring.get_password('dualtext', 'admin')
    if access_token is None:
        s = Session()
        username = click.prompt('Please enter your username')
        pw = click.prompt('Password', hide_inpute=True)
        access_token = s.login(username, pw)
        keyring.set_password('dualtext', username, token)
    ctx.obj['Token'] = access_token

@cli.command('mkproj')
@click.option('--search/--no-search', default=False)
@click.option('--project-data',
        help='data to create a project from',
        type=click.File('r'),
        default=sys.stdin)
@click.pass_context
def make_project(ctx, project_data, search):
    print('Starting to create a project...')
    token = ctx.obj['Token']
    s = Session()
    s = s.set_token(token)
    p = Project(s)
    with project_data:
        data = json.loads(project_data.read())
    if (search):
        proj = p.create_from_documents(data, task_size=100)
    else:
        proj = p.create_from_scratch(data, task_size=100)
    print('Finished creating the project. Project id is {}'.format(proj['id']))

