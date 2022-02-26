import click
import json
from cli_auth import authenticate


def list_resources(entity, out, name_key='name', json_output=False, **kwargs):
    s = authenticate()
    initialized_entity = entity(s)
    resources = initialized_entity.list_resources(kwargs)

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

