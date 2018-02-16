from .constants import *
from json import loads as jloads


class UnparsableError(Exception):
    pass


def parse(tool_type, schema):
    schema = {k: v for k, v in schema}
    if tool_type == [KRAKEN, METAPHLAN2]:
        return parse_mpa(schema['mpa'])
    elif tool_type == HMP_SITES:
        return jloads(schema['metaphlan2'])
    elif tool_type == MICROBE_CENSUS:
        return parse_microbe_census(schema['stats'])
    elif tool_type == SHORTBRED_AMRS:
        return parse_shortbred_table(schema['table'])
    elif tool_type == RESISTOME_AMRS:
        return parse_resistome_tables(schema['gene'], schema['group'],
                                      schema['classus'], schema['mech'])
    elif tool_type == READ_CLASS_PROPS:
        return jloads(schema['json'])
    elif tool_type == READ_STATS:
        return jloads(schema['json'])
    elif tool_type == MICROBE_DIRECTORY:
        return jloads(schema['json'])
    elif tool_type == ALPHA_DIVERSITY:
        return jloads(schema['json'])
    elif tool_type == HUMANN2:
        geneTbl = parse_humann2_table(schema['genes'])
        pathTbl = parse_humann2_pathways(schema['path_abunds'],
                                         schema['path_cov'])
        return {'genes': geneTbl, 'pathways': pathTbl}
    elif tool_type == HUMANN2_NORMALIZED:
        normTbl = parse_humann2_table(schema['read_depth_norm_genes'])
        agsTbl = parse_humann2_table(schema['ags_norm_genes'])
        return {'read_norm': normTbl, 'ags_norm': agsTbl}
    elif tool_type in[METHYLS, VFDB]:
        return parse_gene_table(schema['table'])
    else:
        raise UnparsableError('{}, {}'.format(tool_type, file_type))


def parse_shortbred_table(table_file):
    pass


def parse_resistome_tables(gene_table, group_table,
                           classus_table, mech_table):
    pass


def parse_humann2_table(table_file):
    pass


def parse_humann2_pathways(path_abunds, path_covs):
    pass


def parse_gene_table(gene_Table):
    pass


def parse_mpa(mpa_file):
    data = []
    with open(mpa_file) as mf:
        for line in mf:
            line = line.strip()
            if line[0] == '#':
                continue
            taxa, abund = line.split('\t')
            row = {
                TAXON_KEY: parts[taxon_column_index],
                ABUNDANCE_KEY: float(parts[abundance_column_index]),
            }
            data.append(row)
    return data


def parse_microbe_census(input_file):
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
