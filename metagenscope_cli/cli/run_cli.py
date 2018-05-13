"""CLI to run commands on MGS server."""

from sys import stderr
import click

from .cli import main
from .utils import add_authorization


@main.group()
def run():
    """Run actions on the server."""
    pass


@run.group()
def middleware():
    """Run middleware."""
    pass


@middleware.command(name='group')
@add_authorization()
@click.argument('group_uuid')
def group_middleware(uploader, group_uuid):
    """Run middleware for a group."""
    response = uploader.knex.post(f'/api/v1/sample_groups/{group_uuid}/middleware', {})
    click.echo(response)


@middleware.command(name='sample')
@add_authorization()
@click.argument('sample_name')
def sample_middleware(uploader, sample_name):
    """Run middleware for a sample."""
    response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
    sample_uuid = response['data']['sample_uuid']
    print(f'{sample_name} :: {sample_uuid}', file=stderr)
    response = uploader.knex.post(f'/api/v1/samples/{sample_uuid}/middleware', {})
    click.echo(response)
