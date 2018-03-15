"""Use to upload data sets to the MetaGenScope web platform."""
import click
import datasuper as ds
from .utils import *
from metagenscope_cli.tools.parsers import parse, UnparsableError
from metagenscope_cli.network import Knex, Uploader
from sys import stderr
from requests.exceptions import HTTPError


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


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
    print(response.json()['auth_token'])


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
    handle_uploader_warnings(uploader, verbose=verbose)

    def getsname(fname):
        return fname.split('/')[-1].split('.')[0]

    def getrtype(fname):
        return fname.split('/')[-1].split('.')[1]

    def getfiletype(fname):
        return fname.split('/')[-1].split('.')[2]

    def getrname(fname):
        return getsname(fname) + '::' + getrtype(fname)

    rfiles = {}
    for rfile in result_files:
        sname = getsname(rfile)
        rtype = getrtype(rfile)
        ftype = getfiletype(rfile)

        try:
            try:
                rfiles[sname][rtype][ftype] = rfile
            except KeyError:
                rfiles[sname][rtype] = {ftype: rfile}
        except KeyError:
            rfiles[sname] = {rtype: {ftype: rfile}}

    for sname, rtypeDict in rfiles.items():
        response = uploader.create_sample(sname, group_id=group)
        #handle_uploader_response(response, verbose=verbose)

        for rtype, schema in rtypeDict.items():
            try:
                data = parse(rtype, schema)
                response = uploader.upload_sample_result(sname,
                                                         getrname(rfile),
                                                         rtype,
                                                         data)
                #handle_uploader_response(response, verbose=verbose)
            except UnparsableError as ue:
                raise
            except HTTPError:
                print('http error', file=stderr)
