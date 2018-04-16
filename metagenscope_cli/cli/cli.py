"""Use to upload data sets to the MetaGenScope web platform."""

import click
from requests.exceptions import HTTPError

from metagenscope_cli.network import Knex, Uploader
from metagenscope_cli.network.token_auth import TokenAuth
from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .utils import warn_missing_auth, batch_upload


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(host, username, user_email, password):
    """Register as a new MetaGenScope user."""
    authenticator = Authenticator(host=host)
    try:
        jwt_token = authenticator.register(username, user_email, password)
        click.echo(f'JWT Token: {jwt_token}')
    except HTTPError as http_error:
        click.echo(f'There was an error with registration: {http_error}', err=True)

    # TODO: ask to persist JWT here


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('user_email')
@click.argument('password')
def login(host, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    authenticator = Authenticator(host=host)
    try:
        jwt_token = authenticator.login(user_email, password)
        click.echo(f'JWT Token: {jwt_token}')
    except HTTPError as http_error:
        click.echo(f'There was an error logging in: {http_error}', err=True)

    # TODO: ask to persist JWT here


@main.command()
@click.option('-h', '--host', default=None)
@click.option('-a', '--auth-token', default=None)
def status(host, auth_token):
    """Get user status."""
    try:
        auth = TokenAuth(jwt_token=auth_token)
    except KeyError:
        warn_missing_auth()

    knex = Knex(token_auth=auth, host=host)
    response = knex.get('/api/v1/auth/status')
    click.echo(response)


@main.group()
def upload():
    """Handle different types of uploads."""
    pass

@upload.command()
@click.option('-h', '--host', default=None)
@click.option('-a', '--auth-token', default=None)
@click.option('-g', '--group', default=None)
@click.option('-v', '--verbose', default=False)
def datasuper(host, auth_token, group, verbose):
    """Upload all samples from DataSuper repo."""
    try:
        auth = TokenAuth(jwt_token=auth_token)
    except KeyError:
        warn_missing_auth()
    knex = Knex(token_auth=auth, host=host)
    uploader = Uploader(knex=knex)

    sample_source = DataSuperSource()
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)


@upload.command()
@click.option('-h', '--host', default=None)
@click.option('-a', '--auth-token', default=None)
@click.option('-g', '--group', default=None)
@click.option('-v', '--verbose', default=False)
@click.argument('result_files', nargs=-1)
def files(host, auth_token, group, verbose, result_files):
    """Upload all samples from llist of tool result files."""
    try:
        auth = TokenAuth(jwt_token=auth_token)
    except KeyError:
        warn_missing_auth()
    knex = Knex(token_auth=auth, host=host)
    uploader = Uploader(knex=knex)

    sample_source = FileSource(files=result_files)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)
