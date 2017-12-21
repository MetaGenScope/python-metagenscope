"""Use to upload data sets to the MetaGenScope web platform."""
import click

from metagenscope_cli.hello import hello
from metagenscope_cli.tools.metaphlan2 import metaphlan2
from metagenscope_cli.tools.kraken import kraken
from metagenscope_cli.tools.nanopore import nanopore
from metagenscope_cli.tools.microbe_census import microbe_census
from metagenscope_cli.tools.reads_classified import reads_classified
from metagenscope_cli.tools.hmp_site import hmp_site


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


main.add_command(hello)
main.add_command(metaphlan2)
main.add_command(kraken)
main.add_command(nanopore)
main.add_command(microbe_census)
main.add_command(reads_classified)
main.add_command(hmp_site)
