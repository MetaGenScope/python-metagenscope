"""Upload metaphlan2 results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import upload_command, tsv_to_dict
from metagenscope_cli.tools.constants import TAXON_KEY, ABUNDANCE_KEY


def metaphlan2_data(input_file, taxon_column, abundance_column):
    """Ingest kraken results file."""
    tsv_data = tsv_to_dict(input_file)

    # Require valid taxon column name
    if taxon_column not in tsv_data['column_names']:
        error_message = 'Input .tsv file missing specified taxon column name: {0}'
        raise click.ClickException(error_message.format(taxon_column))

    # Require valid abundance column name
    if abundance_column not in tsv_data['column_names']:
        error_message = 'Input .tsv file missing specified abundance column name: {0}'
        raise click.ClickException(error_message.format(abundance_column))

    def normalize_data(raw_dict):
        """Convert supplied column names to standard column names expected by MetaGenScope."""
        return {
            TAXON_KEY: raw_dict[taxon_column],
            ABUNDANCE_KEY: float(raw_dict[abundance_column]),
        }

    data = [normalize_data(row) for row in tsv_data['data']]

    return data


@upload_command(tool_name='metaphlan2')
@click.option('--taxon-column', '-t', default='#SampleID', help='The taxon column name.')
@click.option('--abundance-column', '-a',
              default='Metaphlan2_Analysis',
              help='The abundance column name.')
def metaphlan2(input_file, taxon_column, abundance_column):
    """Upload metaphlan2 results to the MetaGenScope web platform."""
    return metaphlan2_data(input_file, taxon_column, abundance_column)
