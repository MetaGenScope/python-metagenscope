"""Parsers for different Tool Result types."""

from json import loads

import click

from .constants import *  # pylint:disable=wildcard-import,unused-wildcard-import


class UnparsableError(Exception):
    """Custom exception signaling an unknown Tool Result type."""
    pass


def jloads(fname):
    """Load JSON file into python dictionary."""
    return loads(open(fname).read())


def parse(tool_type, schema):  # pylint: disable=too-many-return-statements,too-many-branches
    """Parse schema as tool_type."""
    if not isinstance(schema, dict):
        schema = {k: v for k, v in schema}

    json_tools = [ALPHA_DIVERSITY, MICROBE_DIRECTORY,
                  READ_STATS]
    if tool_type in json_tools:
        return jloads(schema['json'])
    elif tool_type == READ_CLASS_PROPS:
        return jloads(schema['json'])['totals']
    elif tool_type == HMP_SITES:
        return jloads(schema['metaphlan2'])
    elif tool_type == MICROBE_CENSUS:
        return parse_microbe_census(schema['stats'])
    elif tool_type in [KRAKEN, METAPHLAN2]:
        return {
            'taxa': parse_mpa(schema['mpa'])
        }
    elif tool_type == KRAKENHLL:
        return {
            'taxa': parse_mpa(schema['report'])
        }
    elif tool_type == BETA_DIVERSITY:
        return {
            'data': jloads(schema['json']),
        }
    elif tool_type in [METHYLS, VFDB, AMR_GENES]:
        return {
            'genes': parse_gene_table(schema['table']),
        }
    elif tool_type == MACROBES:
        return {
            'macrobes': jloads(schema['tbl']),
        }
    elif tool_type == ANCESTRY:
        return {
            'populations': parse_key_val_file(schema['table']),
        }

    elif tool_type == HUMANN2:
        return {
            'pathways': parse_humann2_pathways(
                schema['path_abunds'],
                schema['path_cov']
            ),
        }
    elif tool_type == HUMANN2_NORMALIZED:
        return {
            'genes': parse_humann2_tables(
                schema['read_depth_norm_genes'],
                schema['ags_norm_genes'],
            ),
        }
    elif False and tool_type == RESISTOME_AMRS:
        return parse_resistome_tables(
            schema['gene'],
            schema['group'],
            schema['classus'],
            schema['mech']
        )

    raise UnparsableError(f'{tool_type}, {schema}')


def scrub_keys(key):
    """Replace periods (restricted by Mongo) with underscores."""
    return '_'.join(key.split('.'))


def tokenize(file_name, skip=0, sep='\t', skipchar='#'):
    """Tokenize a tabular file."""
    with open(file_name) as file:
        for _ in range(skip):
            file.readline()
        for line in file:
            stripped = line.strip()
            if stripped[0] == skipchar:
                continue
            tkns = stripped.split(sep)
            if len(tkns) >= 2:
                yield tkns


def parse_key_val_file(filename,                                # pylint:disable=too-many-arguments
                       skip=0, skipchar='#', sep='\t',
                       kind=float, key_column=0, val_column=1):
    """Parse a key-value-type file."""
    tokens = tokenize(filename, skip=skip, sep=sep, skipchar=skipchar)
    out = {scrub_keys(token[key_column]): kind(token[val_column])
           for token in tokens}
    return out


def parse_resistome_tables(gene_table, group_table,
                           classus_table, mech_table):
    """Parse a resistome table file."""
    result = {
        'genes': parse_key_val_file(gene_table,
                                    key_column=1, val_column=2,
                                    skip=1, kind=int),
        'groups': parse_key_val_file(group_table,
                                     key_column=1, val_column=2,
                                     skip=1, kind=int),
        'classus': parse_key_val_file(classus_table,
                                      key_column=1, val_column=2,
                                      skip=1, kind=int),
        'mechanism': parse_key_val_file(mech_table,
                                        key_column=1, val_column=2,
                                        skip=1, kind=int),
    }

    return result


def parse_humann2_tables(rpkm_file, rpkmg_file):
    """Ingest Humann2 table file."""
    rpkms = parse_key_val_file(rpkm_file)
    rpkmgs = parse_key_val_file(rpkmg_file)
    data = {}
    rpkms = [(gene, rpkm) for gene, rpkm in rpkms.items()]
    rpkms = sorted(rpkms, key=lambda x: -x[1])[:TOP_N_FILTER]
    for gene, rpkm in rpkms:
        row = {
            RPK_KEY: rpkm,  # hack since rpk does not matter
            RPKM_KEY: rpkm,
            RPKMG_KEY: rpkmgs[gene],
        }
        data[gene] = row
    return data


def parse_humann2_pathways(path_abunds, path_covs):
    """Ingest Humann2 pathways results file."""
    path_abunds = parse_key_val_file(path_abunds)
    path_covs = parse_key_val_file(path_covs)
    data = {}
    for path, abund in path_abunds.items():
        cov = path_covs[path]
        row = {
            ABUNDANCE_KEY: abund,
            COVERAGE_KEY: cov
        }
        data[path] = row
    return data


def parse_gene_table(gene_table):
    """Return a parsed gene quantification table."""
    data = {}
    with open(gene_table) as gfile:
        gfile.readline()
        for line in gfile:
            tkns = line.strip().split(',')
            gene_name = tkns[0]
            rpk = float(tkns[1])
            rpkm = float(tkns[2])
            rpkmg = float(tkns[3])
            row = {
                RPK_KEY: float(tkns[1]),
                RPKM_KEY: float(tkns[2]),
                RPKMG_KEY: float(tkns[3]),
            }
            data[scrub_keys(gene_name)] = row
    data = [(key, val) for key, val in data.items()]
    data = sorted(data, key=lambda x: -x[1][RPKM_KEY])[:TOP_N_FILTER]
    data = {key: val for key, val in data}
    return data


def parse_mpa(mpa_file):
    """Ingest MPA results file."""
    data = [(taxa, val) for taxa, val in parse_key_val_file(mpa_file).items()]
    data = sorted(data, key=lambda x: -x[1])[:TOP_N_FILTER]
    return {key: val for key, val in data}

def parse_microbe_census(input_file):
    """Ingest microbe census results file."""
    data = {}
    with open(input_file) as file:
        for line in file:
            parts = line.strip().split()
            for key in [AGS_KEY, TOTAL_BASES_KEY, GENOME_EQUIVALENTS_KEY]:
                if parts and key in parts[0]:
                    if key == TOTAL_BASES_KEY:
                        data[key] = int(parts[1])
                    else:
                        data[key] = float(parts[1])
    # Require valid values
    for key in [AGS_KEY, TOTAL_BASES_KEY, GENOME_EQUIVALENTS_KEY]:
        if key not in data:
            raise click.ClickException('Missing {0}!'.format(key))

    return data
