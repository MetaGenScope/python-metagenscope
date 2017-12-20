"""Use to upload data sets to the MetaGenScope web platform."""
import click

from metagenscope_cli.metaphlan2 import metaphlan2
from metagenscope_cli.kraken import kraken


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


main.add_command(hello)
main.add_command(metaphlan2)
main.add_command(kraken)
