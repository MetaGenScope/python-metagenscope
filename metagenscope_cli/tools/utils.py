"""Utility methods for CLI tool."""

import click
import requests
import json

from metagenscope_cli.network.token_auth import TokenAuth


def tsv_to_dict(input_tsv):
    """Convert tsv file to list of dictionaries from column name to value."""
    headerline = input_tsv.readline()
    column_names = headerline.rstrip("\n").split("\t")

    data = []

    for line in iter(input_tsv):
        parts = line.rstrip("\n").split("\t")
        row = dict(zip(column_names, parts))
        data.append(row)

    return {
        'column_names': column_names,
        'data': data,
    }


def deliver_payload(payload, auth_token, verbose=False):
    """Deliver a payload to MetaGenScope backend."""
    url = 'http://www.emptyfish.net/api/v1/tools'
    headers = {'Accept': 'application/json'}
    auth = None
    if auth_token is not None:
        auth = TokenAuth(auth_token)
    else:
        click.secho('Warning: Skipping authentication', fg='yellow')

    click.echo('Submitting {0} payload.'.format(payload['tool_name']))
    if verbose:
        click.echo(json.dumps(payload))

    request = requests.post(url, headers=headers, auth=auth, json=payload)

    if request.status_code == requests.codes['created']:
        click.secho('Success: submitted result.', fg='green')
    else:
        error_message = 'MetaGenScope encountered a {0} response.'.format(request.status_code)
        click.secho(error_message, fg='red')
        if verbose:
            try:
                click.secho(request.json())
            except ValueError:
                # Invalid JSON in response
                for line in request.text.splitlines():
                    click.secho("    {0}".format(line), fg='red')
            except Exception as exception:
                click.secho("\tException type: {0}".format(type(exception)), fg='red')
                click.secho("\tException args: {0}".format(exception.args), fg='red')
