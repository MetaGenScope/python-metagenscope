import pandas as pd


def parse_metadata_from_csv(csv_filename):
    df = pd.read_csv(csv_filename, index_col=0)
    return df.to_dict(orient='index')
