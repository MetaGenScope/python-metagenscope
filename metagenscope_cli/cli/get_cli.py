"""CLI to get data from a MetaGenScope Server."""

import click

from .utils import add_authorization


@click.group()
def get():
    """Get data from the server."""
    pass


@get.group()
def uuids():
    """Get UUIDs from the server."""
    pass


def report_uuid(name, uuid):
    """Report a uuid to the user."""
    click.echo(f'{name}\t{uuid}')


@uuids.command(name='samples')
@add_authorization()
@click.argument('sample_names', nargs=-1)
def sample_uuids(uploader, sample_names):
    """Get UUIDs for the given sample names."""
    for sample_name in sample_names:
        response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
        report_uuid(response['data']['sample_name'],
                    response['data']['sample_uuid'])


@uuids.command(name='groups')
@add_authorization()
@click.argument('sample_group_names', nargs=-1)
def sample_group_uuids(uploader, sample_group_names):
    """Get UUIDs for the given sample groups."""
    for sample_group_name in sample_group_names:
        response = uploader.knex.get(f'/api/v1/sample_groups/getid/{sample_group_name}')
        report_uuid(response['data']['sample_group_name'],
                    response['data']['sample_group_uuid'])
