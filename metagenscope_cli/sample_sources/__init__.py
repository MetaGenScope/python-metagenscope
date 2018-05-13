"""Sources for sample data."""

from sys import stderr
from metagenscope_cli.tools.parsers import parse, UnparsableError


class SampleSource(object):
    """Base SampleSource interface."""

    def get_cataloged_files(self):
        """
        Return dictionary of files cataloged by sample and type.

        Returns {<sample_name>: {<result_type>: {<file_type>: <file_path>}}}
        """
        raise NotImplementedError()

    def get_sample_payloads(self):
        """
        Return list of sample payload components (name, endpoint, and body JSON).

        returns {
            <sample_name>: [{
                'result_type': string,
                'data': dict (payload),
            }]
        }
        """
        cataloged_files = self.get_cataloged_files()

        results = {}
        for sample_name, sample_schema in cataloged_files.items():
            results[sample_name] = []
            for result_type, files_dict in sample_schema.items():
                try:
                    data = parse(result_type, files_dict)
                except UnparsableError:
                    print(f'[parse-error] could not parse {result_type}', file=stderr)
                    continue
                except KeyError:
                    print(f'[key-error] {sample_name} :: {result_type}', file=stderr)

                result_payload = {
                    'result_type': result_type,
                    'data': data,
                }
                results[sample_name].append(result_payload)

        return results
