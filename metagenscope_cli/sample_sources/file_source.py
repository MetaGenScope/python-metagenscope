"""Samples from a list of files."""

from metagenscope_cli.sample_sources import SampleSource


def parse_file_path(file_path):
    """Extract file metadata from its path."""
    file_name = file_path.split('/')[-1]
    name_components = file_name.split('.')

    sample_name = name_components[0]
    result_type = name_components[1]
    file_type = name_components[2]

    return sample_name, result_type, file_type


class FileSource(SampleSource):
    """Samples from a list of files."""

    def __init__(self, files):
        """Initialize FileSource from list of files."""
        self.files = files

    def get_cataloged_files(self):
        """Return dictionary of files cataloged by sample and type."""
        catalog = {}
        for file in self.files:
            sample_name, result_type, file_type = parse_file_path(file)

            try:
                try:
                    catalog[sample_name][result_type][file_type] = file
                except KeyError:
                    catalog[sample_name][result_type] = {file_type: file}
            except KeyError:
                catalog[sample_name] = {result_type: {file_type: file}}
        return catalog
