"""Upload kraken results to the MetaGenScope web platform."""

import click

from metagenscope_cli.utils import deliver_payload

TAXON_KEY = 'taxon'
ABUNDANCE_KEY = 'abundance'


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

    root_taxon_total_abundance = 0
    for row in data:
        # Only sum the top level taxon abundances
        if '|' not in row[TAXON_KEY]:
            root_taxon_total_abundance += row[ABUNDANCE_KEY]

    # Normalize abundance
    # Should this actually be happening at this stage? Or instead during visualization step?
    for i in range(0, len(data)):
        data[i][ABUNDANCE_KEY] /= root_taxon_total_abundance

    payload = {
        'tool_name': 'kraken',
        'data': data,
    }

    deliver_payload(payload, auth_token)
