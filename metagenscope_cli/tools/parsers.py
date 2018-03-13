from .constants import *
from json import loads 


class UnparsableError(Exception):
    pass


def jloads(fname):
    return loads(open(fname).read())


def parse(tool_type, schema):
    if type(schema) is not dict:
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
    elif tool_type in [METHYLS, VFDB]:
        return parse_gene_table(schema['table'])
    else:
        raise UnparsableError('{}, {}'.format(tool_type, file_type))


def tokenize(file_name, skip=0, sep='\t', skipchar='#'):
    with open(file_name) as f:
        for _ in range(skip):
            f.readline()
        for line in f:
            stripped = line.strip()
            if stripped[0] == skipchar:
                continue
            tkns = stripped.split(sep)
            yield tkns


def parse_key_val_file(filename,
                       skip=0, skipchar='#', sep='\t',
                       kind=float, val_column=1):
    out = {tkns[0]: kind(tkns[val_column])
           for tkns in tokenize(filename,
                                skip=skip, sep=sep, skipchar=skipchar)
           }
    return out


def parse_shortbred_table(table_file):
    pass


def parse_resistome_tables(gene_table, group_table,
                           classus_table, mech_table):
    out = {'genes': parse_key_val_file(gene_table, skip=1, kind=int),
           'groups': parse_key_val_file(group_table, skip=1, kind=int),
           'classus': parse_key_val_file(classus_table, skip=1, kind=int),
           'mechanism': parse_key_val_file(mech_table, skip=1, kind=int),
           }
    return out


def parse_humann2_table(table_file):
    data = [{GENE_KEY: gene, ABUNDANCE_KEY: abund}
            for gene, abund in parse_key_val_file(table_file)]
    return data


def parse_humann2_pathways(path_abunds, path_covs):
    path_abunds = parse_key_val_file(path_abunds),
    path_covs = parse_key_val_file(path_covs)
    data = []
    for path, abund in path_abunds.items():
        cov = path_covs[path]
        row = {
            PATHWAY_KEY: path,
            ABUNDANCE_KEY: abund,
            COVERAGE_KEY: cov
        }
        data.append(row)
    return data


def parse_gene_table(gene_table):
    '''Return a parsed gene quantification table.'''
    with open(gene_table) as gt:
        gene_names = gt.readline().strip().split(',')[1:]
        rpks = gt.readline().strip().split(',')[1:]
        rpkms = gt.readline().strip().split(',')[1:]
        rpkmgs = gt.readline().strip().split(',')[1:]

    data = []
    for i, gene_name in enumerate(gene_names):
        row = {
            GENE_ID: gene_name,
            RPK_KEY: rpks[i],
            RPKM_KEY: rpkms[i],
            RPKMG_KEY: rpkmgs[i],
        }
        data.append(row)
    return data


def parse_mpa(mpa_file):
    data = []
    for taxa, val in parse_key_val_file(mpa_file):
        row = {TAXON_KEY: taxa, ABUNDANCE_KEY: val}
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
