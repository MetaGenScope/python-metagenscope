"""Upload reads classified results to the MetaGenScope web platform."""

import json

import click

from metagenscope_cli.tools.utils import upload_command


VIRUS_KEY = 'virus'
ARCHAEA_KEY = 'archaea'
BACTERIA_KEY = 'bacteria'
HOST_KEY = 'host'
UNKNOWN_KEY = 'unknown'


def reads_classified_data(input_file):
    """Ingest reads classified results file."""
    data = json.loads(input_file.read())

    # Validate required values
    for key in [VIRUS_KEY, ARCHAEA_KEY, BACTERIA_KEY, HOST_KEY, UNKNOWN_KEY]:
        if key not in data:
            raise click.ClickException('Missing {0}!'.format(key))

    return data


@upload_command(tool_name='reads_classified')
def reads_classified(input_file):
    """Upload reads classified results to the MetaGenScope web platform."""
    return reads_classified_data(input_file)
