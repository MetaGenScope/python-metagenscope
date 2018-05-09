"""Parsers for different Tool Result types."""

from .constants import *  # pylint:disable=wildcard-import,unused-wildcard-import
from .parser_utils import *  # pylint:disable=wildcard-import,unused-wildcard-import


class UnparsableError(Exception):
    """Custom exception signaling an unknown Tool Result type."""

    pass



JSON_TOOLS = {
    ALPHA_DIVERSITY: 'json',
    MICROBE_DIRECTORY: 'json',
    READ_STATS: 'json',
    READ_CLASS_PROPS: 'json',
    HMP_SITES: 'metaphlan2',
    BETA_DIVERSITY: 'json',
    MACROBES: 'tbl',
}

SIMPLE_PARSE = {
    MICROBE_CENSUS:     (parse_microbe_census, 'stats'),
    KRAKEN:             (parse_mpa, 'mpa'),
    METAPHLAN2:         (parse_mpa, 'mpa'),
    KRAKENHLL:          (parse_mpa, 'report'),
    METHYLS:            (parse_gene_table, 'table'),
    VFDB:               (parse_gene_table, 'table'),
    AMR_GENES:          (parse_gene_table, 'table'),
    ANCESTRY:           (parse_key_val_file, 'table'),
    RESISTOME_AMRS:     (parse_resistome_tables, 'gene', 'group', 'classus', 'mech'),
    HUMANN2:            (parse_humann2_pathways, 'path_abunds', 'path_cov'),
    HUMANN2_NORMALIZED: (parse_humann2_tables, 'read_depth_norm_genes', 'ags_norm_genes'),
}

def parse(tool_type, schema):  # pylint: disable=too-many-return-statements,too-many-branches
    """Parse schema as tool_type."""
    if not isinstance(schema, dict):
        schema = {k: v for k, v in schema}

    if tool_type in JSON_TOOLS:
        key = JSON_TOOLS[tool_type]
        return jloads(schema[key])
    elif tool_type in SIMPLE_PARSE:
        func = SIMPLE_PARSE[tool_type][0]
        fnames = [schema[key] for key in SIMPLE_PARSE[tool_type][1:]]
        return func(*fnames)
    raise UnparsableError(f'{tool_type}, {schema}')



