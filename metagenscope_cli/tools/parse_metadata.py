import pandas as pd


def parse_metadata_from_csv(csv_filename):
    df = pd.DataFrame.from_csv(csv_filename)
    return df.to_dict()
