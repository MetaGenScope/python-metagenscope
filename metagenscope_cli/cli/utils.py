"""Utilities for MetaGenScope CLI."""

import os
from sys import stderr
from datetime import datetime
from functools import wraps

import click
from requests.exceptions import HTTPError

from metagenscope_cli.network import Knex, Uploader
from metagenscope_cli.network.token_auth import TokenAuth
from metagenscope_cli.tools.parse_metadata import parse_metadata_from_csv


def parse_metadata(filename, sample_names):
    """Parse sample metadata."""
    if filename[-4:] == '.csv':
        return parse_metadata_from_csv(filename, sample_names)
    raise ValueError(f'{filename} extension is unsupported')


def warn_missing_auth():
    """Warn user of missing authentication."""
    click.echo('No authenication means provided!', err=True)
    click.echo('You must provide an authentication means either by passing '
               '--auth-token or by persisting a login token to your local '
               'MetaGenScope configuration file (see metagenscope login help).')


def batch_upload(uploader, samples, group_uuid=None, upload_group_name=None):
    """Batch upload a group of tool results, creating a new group for the upload."""
    if group_uuid is None:
        current_time = datetime.now().isoformat()
        if upload_group_name is None:
            upload_group_name = f'upload_group_{current_time}'
        group_uuid = uploader.create_sample_group(upload_group_name)
        click.echo(f'group created: <name: \'{upload_group_name}\' UUID: \'{group_uuid}\'>')

    try:
        results = uploader.upload_all_results(group_uuid, samples)
    except HTTPError as error:
        click.echo('Could not create Sample', err=True)
        click.echo(error, err=True)

    if results:
        click.echo('Upload results:')
        for result in results:
            sample_uuid = result['sample_uuid']
            sample_name = result['sample_name']
            result_type = result['result_type']

            if result['type'] == 'error':
                exception = result['exception']
                click.secho(f'  - {sample_name} ({sample_uuid}): {result_type}',
                            fg='red', err=True)
                click.secho(f'    {exception}', fg='red', err=True)
            else:
                click.secho(f'  - {sample_name} ({sample_uuid}): {result_type}', fg='green')
    click.echo(f'group info: <name: \'{upload_group_name}\' UUID: \'{group_uuid}\'>')


def add_authorization():
    """Add authorization to command."""
    def decorator(command):
        """Empty wrapper around decoration to be consistent with Click style."""
        @click.option('-h', '--host', default=None)
        @click.option('-a', '--auth-token', default=None)
        @wraps(command)
        def wrapper(host, auth_token, *args, **kwargs):
            """Wrap command with authorized Uploader creation."""
            try:
                auth = TokenAuth(jwt_token=auth_token)
            except KeyError:
                warn_missing_auth()

            if host is None:
                try:
                    host = os.environ['MGS_HOST']
                except KeyError:
                    print('No host. Exiting', file=stderr)
                    exit(1)

            knex = Knex(token_auth=auth, host=host)
            uploader = Uploader(knex=knex)

            return command(uploader, *args, **kwargs)
        return wrapper
    return decorator
