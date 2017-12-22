"""Upload kraken results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import upload_command
from metagenscope_cli.tools.constants import TAXON_KEY, ABUNDANCE_KEY


def kraken_data(input_file, taxon_column_index, abundance_column_index):
    """Ingest kraken results file."""
    data = []
    for line in iter(input_file):
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
    for datum in data:
        datum[ABUNDANCE_KEY] /= root_taxon_total_abundance

    return data


@upload_command(tool_name='kraken')
@click.option('--taxon-column-index', '-t', default=0, help='The taxon column index.')
@click.option('--abundance-column-index', '-a', default=1, help='The abundance column index.')
def kraken(input_file, taxon_column_index, abundance_column_index):
    """Upload kraken results to the MetaGenScope web platform."""
    return kraken_data(input_file, taxon_column_index, abundance_column_index)
