"""Use to upload data sets to the MetaGenScope web platform."""

import click
from requests.exceptions import HTTPError

from metagenscope_cli.config import config
from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .utils import batch_upload, add_authorization, parse_metadata


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


def handle_auth_request(request_generator):
    """Perform common authentication request functions."""
    try:
        jwt_token = request_generator()
        click.echo(f'JWT Token: {jwt_token}')

        if click.confirm('Store token for future use (overwrites existing)?'):
            config.set_token(jwt_token)
    except HTTPError as http_error:
        click.echo(f'There was an error with registration: {http_error}', err=True)


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(host, username, user_email, password):
    """Register as a new MetaGenScope user."""
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.register(username, user_email, password)

    handle_auth_request(request_generator)


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('user_email')
@click.argument('password')
def login(host, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.login(user_email, password)

    handle_auth_request(request_generator)


@main.command()
@add_authorization()
def status(uploader):
    """Get user status."""
    response = uploader.knex.get('/api/v1/auth/status')
    click.echo(response)


@main.group()
def get():
    """Get data from the server."""
    pass

@get.command()
@add_authorization()
@click.argument('sample_names', nargs=-1)
def sample_uuids(uploader, sample_names):
    """Get UUIDs for the given sample names."""
    for sample_name in sample_names:
        response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
        click.echo('{}\t{}'.format(response['data']['sample_name'], response['data']['sample_uuid']))

@get.command()
@add_authorization()
@click.argument('sample_group_names', nargs=-1)
def sample_group_uuids(uploader, sample_group_names):
    """Get UUIDs for the given sample groups."""
    for sample_group_name in sample_group_names:
        response = uploader.knex.get(f'/api/v1/sample_groups/getid/{sample_name}')
        click.echo('{}\t{}'.format(response['data']['sample_group_name'], response['data']['sample_group_uuid']))

        
@main.command()
@add_authorization()
@click.argument('sample_names', nargs=-1)
def get_sample_uuids(uploader, sample_names):
    """Get UUIDs for the given sample names."""
    for sample_name in sample_names:
        response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
        response_name = response['data']['sample_name']
        response_uuid = response['data']['sample_uuid']
        click.echo(f'{response_name}\t{response_uuid}')

        
@main.group()
def run():
    """Run actions on the server."""
    pass
        
@run.command()
@add_authorization()
@click.argument('group_uuid')
def middleware(uploader, group_uuid):
    response = uploader.knex.post(f'/sample_groups/{group_uuid}/middleware', {'foo': 'bar'})
    click.echo(response)
        

@main.group()
def upload():
    """Handle different types of uploads."""
    pass


@upload.command()
@add_authorization()
@click.argument('metadata_csv')
def metadata(uploader, metadata_csv):
    """Upload a CSV metadata file."""
    parsed_metadata = parse_metadata(metadata_csv)
    for sample_name, sample_metadata in parsed_metadata.items():
        payload = {
            'sample_name': sample_name,
            'metadata': sample_metadata,
        }
        response = uploader.knex.post('/api/v1/samples/metadata', payload)
        click.echo(response)


@upload.command()
@add_authorization()
@click.option('-g', '--group', default=None)
@click.option('--group-name', default=None)
def datasuper(uploader, group, group_name):
    """Upload all samples from DataSuper repo."""
    sample_source = DataSuperSource()
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group, upload_group_name=group_name)


@upload.command()
@add_authorization()
@click.option('-g', '--group', default=None)
@click.argument('result_files', nargs=-1)
def files(uploader, group, result_files):
    """Upload all samples from llist of tool result files."""
    sample_source = FileSource(files=result_files)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)
