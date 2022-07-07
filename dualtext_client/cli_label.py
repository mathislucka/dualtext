import click
import sys
from label import Label
from cli_crud import list_resources, delete_resource, create_resource, update_resource


@click.group()
def label():
    pass


@label.command('ls')
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
@click.option(
    '--project-id',
    '-p',
    help="The project of which you'd like to list the labels.",
    type=click.INT
)
def list_labels(json_output, out, project_id):
    list_resources(Label, json_output=json_output, out=out, project_id=project_id)


@label.command('create')
@click.option(
    '--project-id',
    '-p',
    help='The project that this label should be created for.',
    type=click.INT,
    default=sys.stdin
)
@click.option(
    '--name',
    '-n',
    help='The name of the label you would like to create.',
    type=str
)
@click.option(
    '--key-code',
    '-k',
    help='The key code that can be used to select the label.'
)
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
def create_label(project_id, out, json_output, key_code, name):
    create_resource(
        Label,
        json_output=json_output,
        out=out,
        params={'project_id': project_id},
        key_code=key_code,
        name=name
    )


@label.command('update')
@click.option(
    '--id',
    'label_id',
    help="The id of the label that you would like to update.",
    type=click.INT
)
@click.option(
    '--project-id',
    '-p',
    help='The project that this label should be updated for.',
    type=click.INT,
    default=sys.stdin
)
@click.option(
    '--name',
    '-n',
    help='The name of the label you would like to create.',
    type=str
)
@click.option(
    '--key-code',
    '-k',
    help='The key code that can be used to select the label.'
)
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
def update_label(label_id, project_id, out, json_output, key_code=None, name=None):
    updated_attributes = {'id': label_id}
    if key_code:
        updated_attributes['key_code'] = key_code
    if name:
        updated_attributes['name'] = name

    update_resource(
        Label,
        json_output=json_output,
        out=out,
        params={'project_id': project_id},
        **updated_attributes
    )