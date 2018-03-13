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
    for sample in repo.sampleTable.getAll():
        response = uploader.create_sample(sample.name,
                                          metadata=sample.metadata)
        handle_uploader_response(response, verbose=verbose)
        for result in sample.results():
            try:
                data = parse(result.resultType(), result.files())
                response = uploader.upload_data(sample.name,
                                                result.name,
                                                result.resultType(),
                                                data)
                handle_uploader_response(response, verbose=verbose)
            except UnparsableError:
                pass


@click.command()
@click.option('-u', '--url')
@click.option('-a', '--auth', default=None)
@click.option('-v', '--verbose', default=False)
@click.argument('result_files', nargs=-1)
def upload_files(url, auth, verbose, result_files):
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
        ftype = getfiletype(fname)

        try:
            try:
                rfiles[sname][rtype][ftype] = rfile
            except KeyError:
                rfiles[sname][rtype] = {ftype: rfile}
        except KeyError:
            rfiles[sname] = {rtype: {ftype: rfile}}

    for sname, rtypeDict in snames.items():
        response = uploader.create_sample(sample.name)
        handle_uploader_response(response, verbose=verbose)

        for rtype, schema in rtypeDict.items():
            try:
                data = parse(rtype, schema)
                response = uploader.upload_data(sname,
                                                getrname(rfile),
                                                rtype,
                                                data)
                handle_uploader_response(response, verbose=verbose)
            except UnparsableError:
                pass
