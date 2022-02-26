import click
from project import Project
from cli_auth import authenticate
from cli_crud import list_resources, delete_resource
import json
import sys


@click.group()
def project():
    pass


@project.command('ls')
@click.option(
    '--json',
    '-j',
    'json_output',
    is_flag=True,
    default=False
)
@click.option(
    "--out",
    help="File to write the output to, omit to display on screen.",
    type=click.File("w"),
    default=sys.stdout,
)
def list_projects(json_output, out):
    list_resources(Project, json_output=json_output, out=out)


@project.command('create')
@click.option('--search/--no-search', default=False)
@click.option(
    '--project-file',
    '-f',
    help='File containing project data.',
    type=click.File('r'),
    default=sys.stdin
)
@click.option(
    '--task-size',
    '-t',
    help='Sets the number of documents for a task. Default is 20.',
    type=click.INT,
    default=20
)
def create(project_file, search, task_size):
    click.echo('Starting to create a project...', err=True)

    s = authenticate()
    p = Project(s)

    with project_file:
        data = json.loads(project_file.read())
    if search:
        proj = p.create_from_documents(data, task_size=task_size)
    else:
        proj = p.create_from_scratch(data, task_size=task_size)

    click.echo('Finished creating the project. Project id is {}'.format(proj['id']), err=True)


@project.command('delete')
@click.option(
    '--project-id',
    '-p',
    help='Id of project that you would like to delete.',
    type=click.INT,
    default=sys.stdin
)
@click.confirmation_option(prompt='Are you sure you want to delete the project?')
def delete_project(project_id):
    delete_resource(Project, entity_id=project_id)


@project.command('download')
@click.option(
    '--project-id',
    '-p',
    help='Id of project that you would like to download from.',
    type=click.INT,
    default=sys.stdin
)
@click.option('--action', '-a', type=str)
@click.option('--finished', 'status', flag_value=True)
@click.option('--notfinished', 'status', flag_value=False)
@click.option('--label', '-l', type=str, multiple=True)
@click.option(
    "--out",
    help="File to write the Output to, omit to display on screen.",
    type=click.File("w"),
    default=sys.stdout,
)
def download_project(project_id, out, action=None, label=None, status=None):
    task_params = {}
    annotation_params = {}
    if action is not None:
        task_params['action'] = action
    if status is not None:
        task_params['is_finished'] = status
    if label is not None:
        annotation_params['label_name'] = list(label)

    s = authenticate()
    p = Project(s)

    click.echo(
        json.dumps(p.get_annotations(project_id, task_params=task_params, annotation_params=annotation_params)),
        file=out
    )