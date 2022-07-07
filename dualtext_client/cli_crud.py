import click
import json
from cli_auth import authenticate


def list_resources(entity, out, name_key='name', json_output=False, **kwargs):
    s = authenticate()
    initialized_entity = entity(s, **kwargs)
    resources = initialized_entity.list_resources()

    if json_output:
        click.echo(json.dumps(resources), file=out)
    else:
        click.echo('ID \t NAME')

        for resource in resources:
            click.echo(f'{resource["id"]} \t {resource[name_key]}')


def delete_resource(entity, entity_id):
    s = authenticate()
    initialized_entity = entity(s)

    response = initialized_entity.delete(entity_id)
    click.echo(response)
    click.echo(f'Deleted {initialized_entity.__class__.__name__} with id {entity_id}.')


def create_resource(entity, out, json_output=False, params=None, **kwargs):
    s = authenticate()
    if params:
        initialized_entity = entity(s, **params)
    else:
        initialized_entity = entity(s)

    response = initialized_entity.create(kwargs)

    click.echo(f'Created {initialized_entity.__class__.__name__}.', err=True)
    if json_output:
        click.echo(json.dumps(response), file=out)
    else:
        for key, value in response.items():
            click.echo(f'{key} \t {value}')


def update_resource(entity, out, params=None, json_output=False, **kwargs):
    s = authenticate()

    if params:
        initialized_entity = entity(s, **params)
    else:
        initialized_entity = entity(s)

    response = initialized_entity.update(kwargs)

    click.echo(f'Updated {initialized_entity.__class__.__name__}.', err=True)
    if json_output:
        click.echo(json.dumps(response), file=out)
    else:
        for key, value in response.items():
            click.echo(f'{key} \t {value}')