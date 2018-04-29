"""Use to upload data sets to the MetaGenScope web platform."""

import click
from requests.exceptions import HTTPError

from metagenscope_cli.config import config
from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .utils import batch_upload, add_authorization


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

        if click.confirm('Store token for future use (overwrites existing)?'):
            config.set_token(jwt_token)
    except HTTPError as http_error:
        click.echo(f'There was an error logging in: {http_error}', err=True)

    # TODO: ask to persist JWT here


@main.command()
@add_authorization()
def status(uploader):
    """Get user status."""
    response = uploader.knex.get('/api/v1/auth/status')
    click.echo(response)


@main.group()
def upload():
    """Handle different types of uploads."""
    pass

@upload.command()
@add_authorization()
@click.option('-g', '--group', default=None)
@click.option('-v', '--verbose', default=False)
def datasuper(uploader, group, verbose):
    """Upload all samples from DataSuper repo."""
    sample_source = DataSuperSource()
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)


@upload.command()
@add_authorization()
@click.option('-g', '--group', default=None)
@click.option('-v', '--verbose', default=False)
@click.argument('result_files', nargs=-1)
def files(uploader, group, verbose, result_files):
    """Upload all samples from llist of tool result files."""
    sample_source = FileSource(files=result_files)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)
