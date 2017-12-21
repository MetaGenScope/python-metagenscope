"""Upload reads classified results to the MetaGenScope web platform."""

import click
import json

from metagenscope_cli.tools.utils import upload_command


VIRUS_KEY = 'virus'
ARCHAEA_KEY = 'archaea'
BACTERIA_KEY = 'bacteria'
HOST_KEY = 'host'
UNKNOWN_KEY = 'unknown'


@upload_command(tool_name='reads_classified')
def reads_classified(input_file):
    """Upload reads classified results to the MetaGenScope web platform."""
    data = json.loads(input_file.read())

    # Validate required values
    for key in [VIRUS_KEY, ARCHAEA_KEY, BACTERIA_KEY, HOST_KEY, UNKNOWN_KEY]:
        if key not in data:
            click.secho('Error: missing {0}!'.format(key), fg='red')
            return

    return data
