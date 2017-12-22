"""Upload microbe census results to the MetaGenScope web platform."""

import click

from metagenscope_cli.tools.utils import upload_command

# Expected input-file content:

# Parameters
# metagenome: [[path].fastq.gz]...
# reads_sampled:  2000000
# trimmed_length: 150
# min_quality:    -5
# mean_quality:   -5
# filter_dups:    False
# max_unknown:    100
#
# Results
# average_genome_size:    70513906.6967
# total_bases:    1709470396
# genome_equivalents: 24.2430249022


AGS_KEY = 'average_genome_size'
TOTAL_BASES_KEY = 'total_bases'
GENOME_EQUIVALENTS_KEY = 'genome_equivalents'


def microbe_census_data(input_file):
    """Ingest microbe census results file."""
    data = {}
    for line in iter(input_file):
        parts = line.rstrip("\n").split("\t")
        for key in [AGS_KEY, TOTAL_BASES_KEY, GENOME_EQUIVALENTS_KEY]:
            if key in parts[0]:
                if key == TOTAL_BASES_KEY:
                    data[key] = int(parts[1])
                else:
                    data[key] = float(parts[1])

    # Require valid values
    for key in [AGS_KEY, TOTAL_BASES_KEY, GENOME_EQUIVALENTS_KEY]:
        if key not in data:
            raise click.ClickException('Missing {0}!'.format(key))

    return data


@upload_command(tool_name='microbe_census')
def microbe_census(input_file):
    """Upload microbe census results to the MetaGenScope web platform."""
    return microbe_census_data(input_file)
