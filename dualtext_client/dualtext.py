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
        pw = click.prompt('Password', hide_input=True)
        s.login(username, pw)
        access_token = s.get_token()
        print(access_token)
        #keyring.set_password('dualtext', username, access_token)
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


@cli.command('dlproj')
@click.option('--project-id',
        help='Id of project that you would like to download from.',
        type=click.INT,
        default=sys.stdin)
@click.option('--action', '-a', type=str)
@click.option('--finished', 'status', flag_value=True)
@click.option('--notfinished', 'status', flag_value=False)
@click.option('--label', '-l', type=str, multiple=True)
@click.pass_context
def download_project(ctx, project_id, action=None, label=None, status=None):
    task_params = {}
    annotation_params = {}
    if action is not None:
        task_params['action'] = action
    if status is not None:
        task_params['is_finished'] = status
    if label is not None:
        annotation_params['label_name'] = list(label)
    token = ctx.obj['Token']
    s = Session()
    s = s.set_token(token)
    p = Project(s)
    click.echo(p.get_annotations(project_id, task_params=task_params, annotation_params=annotation_params))

