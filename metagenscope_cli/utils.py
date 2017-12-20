"""Utility methods for CLI tool."""


def tsv_to_dict(input_tsv):
    """Convert tsv file to list of dictionaries from column name to value."""
    headerline = input_tsv.readline()
    column_names = headerline.rstrip("\n").split("\t")

    data = []

    for line in iter(input_tsv):
        parts = line.rstrip("\n").split("\t")
        row = dict(zip(column_names, parts))
        data.append(row)

    return {
        'column_names': column_names,
        'data': data,
    }
