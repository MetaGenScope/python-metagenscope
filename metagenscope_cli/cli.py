"""Use to upload data sets to the MetaGenScope web platform."""
import click

from metagenscope_cli.utils import tsv_to_dict


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.argument('name', default='world', required=False)
def hello(name, as_cowboy):
    """Hello World entry point."""
    greet = 'Howdy' if as_cowboy else 'Hello'
    click.echo('{0}, {1}.'.format(greet, name))


@click.command()
@click.option('--taxon-column', '-t', default='#SampleID', help='The taxon column name.')
@click.option('--abundance-column', '-a',
              default='Metaphlan2_Analysis',
              help='The abundance column name.')
@click.option('--auth-token', help='JWT for authorization.')
@click.argument('input-tsv', type=click.File('rb'))
def metaphlan2(taxon_column, abundance_column, auth_token, input_tsv):
    """Upload metaphlan2 results to the MetaGenScope web platform."""
    tsv_data = tsv_to_dict(input_tsv)

    # Require valid taxon column name
    if taxon_column not in tsv_data['column_names']:
        error_message = 'Error: input .tsv file missing specified taxon column name: {0}'
        click.secho(error_message.format(taxon_column), fg='red')
        return

    # Require valid abundance column name
    if abundance_column not in tsv_data['column_names']:
        error_message = 'Error: input .tsv file missing specified abundance column name: {0}'
        click.secho(error_message.format(abundance_column), fg='red')
        return

    def normalize_data(raw_dict):
        """Convert supplied column names to standard column names expected by MetaGenScope."""
        return {
            'taxon': raw_dict[taxon_column],
            'abundance': raw_dict[abundance_column],
        }

    data = [normalize_data(row) for row in tsv_data['data']]
    payload = {
        'tool_name': 'metaphlan2',
        'data': data,
    }

    if auth_token is not None:
        click.echo('Using auth token: {0}'.format(auth_token))
    else:
        click.secho('Warning: Skipping authentication', fg='yellow')

    click.echo('Submitting the following metaphlan2 payload:')
    click.echo(payload)


main.add_command(hello)
main.add_command(metaphlan2)
