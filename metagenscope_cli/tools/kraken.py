"""Upload kraken results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import deliver_payload
from metagenscope_cli.tools.constants import KRAKEN_TOOL_NAME, TAXON_KEY, ABUNDANCE_KEY


@click.command()
@click.option('--taxon-column-index', '-t', default=0, help='The taxon column index.')
@click.option('--abundance-column-index', '-a', default=1, help='The abundance column index.')
@click.option('--auth-token', help='JWT for authorization.')
@click.argument('input-tsv', type=click.File('rb'))
def kraken(taxon_column_index, abundance_column_index, auth_token, input_tsv):
    """Upload kraken results to the MetaGenScope web platform."""
    data = []
    for line in iter(input_tsv):
        parts = line.rstrip("\n").split("\t")
        row = {
            TAXON_KEY: parts[taxon_column_index],
            ABUNDANCE_KEY: float(parts[abundance_column_index]),
        }
        data.append(row)

    # Normalize abundance
    # Should this actually be happening at this stage? Or instead during visualization step?
    root_taxon_total_abundance = 0
    for row in data:
        # Only sum the top level taxon abundances
        if '|' not in row[TAXON_KEY]:
            root_taxon_total_abundance += row[ABUNDANCE_KEY]
    for i in range(0, len(data)):
        data[i][ABUNDANCE_KEY] /= root_taxon_total_abundance

    payload = {
        'tool_name': KRAKEN_TOOL_NAME,
        'data': data,
    }

    deliver_payload(payload, auth_token)
