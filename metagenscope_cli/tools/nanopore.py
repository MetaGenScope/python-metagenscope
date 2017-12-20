"""Upload nanopore results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import deliver_payload
from metagenscope_cli.tools.constants import NANOPORE_TOOL_NAME, TAXON_KEY, ABUNDANCE_KEY


@click.command()
@click.option('--taxon-column-index', '-t', default=0, help='The taxon column index.')
@click.option('--abundance-column-index', '-a', default=1, help='The abundance column index.')
@click.option('--auth-token', help='JWT for authorization.')
@click.argument('input-tsv', type=click.File('rb'))
def nanopore(taxon_column_index, abundance_column_index, auth_token, input_tsv):
    """Upload nanopore results to the MetaGenScope web platform."""
    data = []
    for line in iter(input_tsv):
        parts = line.rstrip("\n").split("\t")
        taxon_name = parts[taxon_column_index]
        if '.' not in taxon_name:
            row = {
                TAXON_KEY: taxon_name,
                ABUNDANCE_KEY: float(parts[abundance_column_index]),
            }
            data.append(row)

    payload = {
        'tool_name': NANOPORE_TOOL_NAME,
        'data': data,
    }

    deliver_payload(payload, auth_token)
