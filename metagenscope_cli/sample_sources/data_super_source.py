"""Samples from a DataSuper repository."""

import datasuper as ds

from metagenscope_cli.sample_sources import SampleSource


class DataSuperSource(SampleSource):
    """Samples from a DataSuper repository."""

    def __init__(self, all_samples=True):
        """Initialize a DataSuperSource instance."""
        self.all_samples = all_samples

    def get_cataloged_files(self):
        """Return dictionary of files cataloged by sample and type."""
        repo = ds.Repo.loadRepo()
        samples = repo.sampleTable.getAll()

        catalog = {}
        for sample in samples:
            catalog[sample.name] = {}
            for result in sample.results():
                result_type = result.resultType()
                catalog[sample.name][result_type] = result.files()

        return catalog
