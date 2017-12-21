"""Upload reads classified results to the MetaGenScope web platform."""

import click
import json

from metagenscope_cli.tools.utils import deliver_payload


READS_CLASSIFIED_TOOL_NAME = 'reads_classified'

VIRUS_KEY = 'virus'
ARCHAEA_KEY = 'archaea'
BACTERIA_KEY = 'bacteria'
HOST_KEY = 'host'
UNKNOWN_KEY = 'unknown'


@click.command()
@click.option('--auth-token', help='JWT for authorization.')
@click.argument('input-file', type=click.File('rb'))
def reads_classified(auth_token, verbose, input_file):
    """Upload reads classified results to the MetaGenScope web platform."""
    data = json.loads(input_file.read())

    # Validate required values
    for key in [VIRUS_KEY, ARCHAEA_KEY, BACTERIA_KEY, HOST_KEY, UNKNOWN_KEY]:
        if key not in data:
            click.secho('Error: missing {0}!'.format(key), fg='red')
            return

    payload = {
        'tool_name': READS_CLASSIFIED_TOOL_NAME,
        'data': data,
    }

    deliver_payload(payload, auth_token, verbose)
