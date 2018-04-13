"""Use to upload data sets to the MetaGenScope web platform."""

from sys import stderr

import click
import datasuper as ds
from requests.exceptions import HTTPError

from metagenscope_cli.tools.parsers import parse, UnparsableError
from metagenscope_cli.network import Knex, Uploader

from .utils import handle_uploader_warnings, handle_uploader_response


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


@main.command()
@click.option('-u', '--url')
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(url, username, user_email, password):
    knex = Knex(url).suppress_warnings()
    payload = {
        'username': username,
        'email': user_email,
        'password': password
    }
    response = knex.upload_payload('/api/v1/auth/register', payload)
    print(response.json())


@main.command()
@click.option('-u', '--url')
@click.argument('user_email')
@click.argument('password')
def login(url, user_email, password):
    knex = Knex(url).suppress_warnings()
    payload = {
        'email': user_email,
        'password': password
    }
    response = knex.upload_payload('/api/v1/auth/login', payload)
    print(response.json()['data']['auth_token'])


@main.command()
@click.option('-u', '--url')
@click.option('-a', '--auth', default=None)
def status(url, auth):
    knex = Knex(url, auth=auth)
    handle_uploader_warnings(knex)
    response = knex.get('/api/v1/auth/status')
    print(response.json())


@main.command()
@click.option('-u', '--url')
@click.option('-a', '--auth', default=None)
@click.option('-v', '--verbose', default=False)
def upload(url, auth, verbose):
    uploader = Uploader(url, auth=auth)
    handle_uploader_warnings(uploader, verbose=verbose)
    repo = ds.Repo.loadRepo()
    for sample in repo.sampleTable.getAll():
        response = uploader.create_sample(sample.name,
                                          metadata=sample.metadata)
        handle_uploader_response(response, verbose=verbose)
        for result in sample.results():
            try:
                data = parse(result.resultType(), result.files())
                response = uploader.upload_sample_result(sample.name,
                                                         result.name,
                                                         result.resultType(),
                                                         data)
                handle_uploader_response(response, verbose=verbose)
            except UnparsableError:
                pass


@main.command()
@click.option('-u', '--url')
@click.option('-a', '--auth', default=None)
@click.option('-g', '--group', default=None)
@click.option('-v', '--verbose', default=False)
@click.argument('result_files', nargs=-1)
def upload_files(url, auth, group, verbose, result_files):
    uploader = Uploader(url, auth=auth)
    handle_uploader_warnings(uploader)

    def get_sample_name(file_name):
        return file_name.split('/')[-1].split('.')[0]

    def get_result_type(file_name):
        return file_name.split('/')[-1].split('.')[1]

    def get_file_type(file_name):
        return file_name.split('/')[-1].split('.')[2]

    def get_result_name(file_name):
        return get_sample_name(file_name) + '::' + get_result_type(file_name)

    result_files = {}
    for result_file in result_files:
        sample_name = get_sample_name(result_file)
        result_type = get_result_type(result_file)
        file_type = get_file_type(result_file)

        try:
            try:
                result_files[sample_name][result_type][file_type] = result_file
            except KeyError:
                result_files[sample_name][result_type] = {file_type: result_file}
        except KeyError:
            result_files[sample_name] = {result_type: {file_type: result_file}}

    for sample_name, result_type_dict in result_files.items():
        response = uploader.create_sample(sample_name, group_id=group)

        for result_type, schema in result_type_dict.items():
            try:
                data = parse(result_type, schema)
                response = uploader.upload_sample_result(sample_name,
                                                         get_result_name(result_file),
                                                         result_type,
                                                         data)
            except UnparsableError:
                raise
            except HTTPError:
                print('http error', file=stderr)
