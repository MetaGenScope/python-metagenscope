"""Utility methods for CLI tool."""

import click
import json


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


def deliver_payload(payload, auth_token):
    """Deliver a payload to MetaGenScope backend."""
    if auth_token is not None:
        click.echo('Using auth token: {0}'.format(auth_token))
    else:
        click.secho('Warning: Skipping authentication', fg='yellow')

    click.echo('Submitting the following {0} payload:'.format(payload['tool_name']))
    click.echo(json.dumps(payload))
