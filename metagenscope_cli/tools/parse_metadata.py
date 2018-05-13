"""Parser for Sample metadata."""

import pandas as pd

NA_TOKEN = 'n/a'


def parse_metadata_from_csv(csv_filename, sample_names):
    """Parse sample metadata from a .csv file."""
    df = pd.read_csv(csv_filename, index_col=None, dtype=str).fillna(NA_TOKEN)
    colnames = list(df.columns.values)
    df = df.set_index(colnames[0])
    tbl = df.to_dict(orient='index')
    for sample_name in sample_names:
        if sample_name not in tbl:
            tbl[sample_name] = {colname: NA_TOKEN for colname in colnames}
    df = pd.DataFrame.from_dict(tbl, orient='index').fillna(NA_TOKEN)
    return df.to_dict(orient='index')

