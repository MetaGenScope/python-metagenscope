"""Utilities for MetaGenScope CLI."""

import click
import requests

from metagenscope_cli.config import config


def handle_uploader_warnings(uploader):
    if uploader.warnings() == 'unknown_token':
        if click.confirm('Store token for future use (overwrites existing)?'):
            try:
                config.set_token(str(uploader.auth))
            except AttributeError:
                config.set_token(str(uploader.knex.auth))
            uploader.suppress_warnings()
        elif click.confirm('Continue with provided token?', abort=True):
            uploader.suppress_warnings()
    elif uploader.warnings() == 'no_auth':
        click.secho('Warning: Skipping authentication', fg='yellow')
        uploader.suppress_warnings()
    return uploader


def handle_uploader_response(request, verbose=False):
    if request.status_code == requests.codes['created']:
        click.secho('Success: submitted result.', fg='green')
    else:
        error_message = 'Bad Response: {0} '.format(request.status_code)
        click.secho(error_message, fg='red')
        if verbose:
            try:
                click.secho(request.json())
            except ValueError:
                # Invalid JSON in response
                for line in request.text.splitlines():
                    click.secho("    {0}".format(line), fg='red')
