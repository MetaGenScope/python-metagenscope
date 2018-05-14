"""Parsing utilities."""

from json import loads

from .constants import (RPK_KEY, RPKM_KEY, RPKMG_KEY, TOP_N_FILTER, ABUNDANCE_KEY,
                        COVERAGE_KEY, GENOME_EQUIVALENTS_KEY, AGS_KEY, TOTAL_BASES_KEY)


def jloads(fname):
    """Load JSON file into python dictionary."""
    return loads(open(fname).read())


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
            assert False, 'Missing key in MicrobeCensus'

    return data
