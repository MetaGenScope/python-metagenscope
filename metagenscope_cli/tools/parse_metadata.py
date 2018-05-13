"""Parser for Sample metadata."""

import pandas as pd


def parse_metadata_from_csv(csv_filename):
    """Parse sample metadata from a .csv file."""
    data_frame = pd.DataFrame.from_csv(csv_filename)
    return data_frame.to_dict()
