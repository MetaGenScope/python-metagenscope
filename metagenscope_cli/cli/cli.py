"""Use to upload data sets to the MetaGenScope web platform."""
import click
import datasuper as ds
from .utils import *
from metagenscope_cli.tools.parsers import parse, UnparsableError


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


@click.command()
@click.option('-u', '--url')
@click.option('-a', '--auth', default=None)
@click.option('-v', '--verbose', default=False)
def upload(url, auth, verbose):
    uploader = Uploader(url, auth=auth)
    handle_uploader_warnings(uploader, verbose=verbose)
    repo = ds.Repo.loadRepo()
    for result in repo.resultTable.getAll():
        try:
            data = parse(result.resultType(),
                         result.files())
            response = uploader.upload_data(result.name,
                                            result.resultType(),
                                            data)
            handle_uploader_response(response, verbose=verbose)
        except UnparsableError:
            pass
