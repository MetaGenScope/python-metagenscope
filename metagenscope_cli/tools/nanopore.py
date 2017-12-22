"""Upload nanopore results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import upload_command
from metagenscope_cli.tools.constants import TAXON_KEY, ABUNDANCE_KEY


def nanopore_data(input_file, taxon_column_index, abundance_column_index):
    """Ingest nanopore results file."""
    data = []
    for line in iter(input_file):
        parts = line.rstrip("\n").split("\t")
        taxon_name = parts[taxon_column_index]
        if '.' not in taxon_name:
            row = {
                TAXON_KEY: taxon_name,
                ABUNDANCE_KEY: float(parts[abundance_column_index]),
            }
            data.append(row)

    return data


@upload_command(tool_name='nanopore')
@click.option('--taxon-column-index', '-t', default=0, help='The taxon column index.')
@click.option('--abundance-column-index', '-a', default=1, help='The abundance column index.')
def nanopore(input_file, taxon_column_index, abundance_column_index):
    """Upload nanopore results to the MetaGenScope web platform."""
    return nanopore_data(input_file, taxon_column_index, abundance_column_index)
