"""CLI to upload data to a MetaGenScope Server."""

import click
from sys import stderr

from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .cli import main
from .utils import batch_upload, add_authorization, parse_metadata


@main.group()
def upload():
    """Handle different types of uploads."""
    pass


@upload.command()
@add_authorization()
@click.argument('metadata_csv')
@click.argument('sample_names', nargs=-1)
def metadata(uploader, metadata_csv, sample_names):
    """Upload a CSV metadata file."""
    parsed_metadata = parse_metadata(metadata_csv, sample_names)
    for sample_name, metadata in parsed_metadata.items():
        payload = {
            'sample_name': str(sample_name),
            'metadata': metadata,
        }
        try:
            response = uploader.knex.post('/api/v1/samples/metadata', payload)
            click.echo(response)
        except Exception:
            print(f'[upload-metadata-error] {sample_name}', file=stderr)


@upload.command()
@add_authorization()
@click.option('-g', '--group', default=None)
@click.option('--group-name', default=None)
@click.option('-v', '--verbose', default=False)
def datasuper(uploader, group, group_name, verbose):
    """Upload all samples from DataSuper repo."""
    sample_source = DataSuperSource()
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group, upload_group_name=group_name)


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
