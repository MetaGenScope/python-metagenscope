"""Parsers for different Tool Result types."""

from . import parser_utils as utils, constants as const


class UnparsableError(Exception):
    """Custom exception signaling an unknown Tool Result type."""

    pass


JSON_TOOLS = {
    const.ALPHA_DIVERSITY: 'json',
    const.MICROBE_DIRECTORY: 'json',
    const.READ_STATS: 'json',
    const.READ_CLASS_PROPS: 'json',
    const.HMP_SITES: 'metaphlan2',
    const.BETA_DIVERSITY: 'json',
    const.MACROBES: 'tbl',
}

SIMPLE_PARSE = {
    const.MICROBE_CENSUS:     (utils.parse_microbe_census, 'stats'),
    const.KRAKEN:             (utils.parse_mpa, 'mpa'),
    const.METAPHLAN2:         (utils.parse_mpa, 'mpa'),
    const.KRAKENHLL:          (utils.parse_mpa, 'report'),
    const.METHYLS:            (utils.parse_gene_table, 'table'),
    const.VFDB:               (utils.parse_gene_table, 'table'),
    const.AMR_GENES:          (utils.parse_gene_table, 'table'),
    const.ANCESTRY:           (utils.parse_key_val_file, 'table'),
    const.RESISTOME_AMRS:     (utils.parse_resistome_tables,
                               'gene', 'group', 'classus', 'mech'),
    const.HUMANN2:            (utils.parse_humann2_pathways,
                               'path_abunds', 'path_cov'),
    const.HUMANN2_NORMALIZED: (utils.parse_humann2_tables,
                               'read_depth_norm_genes', 'ags_norm_genes'),
}


def parse(tool_type, schema):
    """Parse schema as tool_type."""
    if tool_type in JSON_TOOLS:
        key = JSON_TOOLS[tool_type]
        return utils.jloads(schema[key])
    elif tool_type in SIMPLE_PARSE:
        func = SIMPLE_PARSE[tool_type][0]
        fnames = [schema[key] for key in SIMPLE_PARSE[tool_type][1:]]
        return func(*fnames)
    raise UnparsableError(f'{tool_type}, {schema}')
