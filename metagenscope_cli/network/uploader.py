"""Uploader class handles uploading samples to a server."""

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sys import stderr

from requests.exceptions import HTTPError


class Uploader:
    """Uploader class handles uploading samples to a server."""

    def __init__(self, knex):
        """Initialize Uploader instance."""
        self.knex = knex

    def create_sample_group(self, group_name):
        """Create Sample Group on remote server."""
        payload = {'name': group_name}
        response = self.knex.post('/api/v1/sample_groups', payload)
        group_uuid = response['data']['sample_group']['uuid']
        return group_uuid

    def create_sample(self, sample_name, group_uuid, metadata={}):  # pylint: disable=dangerous-default-value
        """Create Sample on remote server."""
        payload = {
            "name": sample_name,
            "sample_group_uuid": group_uuid,
            "metadata": metadata,
        }
        try:
            response = self.knex.post('/api/v1/samples', payload)
            sample_uuid = response['data']['sample']['uuid']
        except HTTPError:
            response = self.knex.get(f'/api/v1/samples/getid/{sample_name}')
            sample_uuid = response['data']['sample_uuid']
        return sample_uuid

    def upload_sample_result(self, sample_uuid, result_type, data, dryrun=False):
        """Upload a tool result of specified type to existing sample."""
        endpoint = f'/api/v1/samples/{sample_uuid}/{result_type}'
        if dryrun:
            endpoint += '?dryrun=true'
        response = self.knex.post(endpoint, data)
        return response

    def get_try_upload(self, sample_uuid, sample_name,  # pylint:disable=too-many-arguments
                       result_type, result, data, dryrun):
        """Return a function that will attempt an upload when called."""

        def try_upload():
            """Attempt an upload, return the result."""
            date_now = datetime.now()
            try:
                print(f'[uploader {date_now}] uploading {sample_name} :: {result_type}',
                      file=stderr)
                self.upload_sample_result(sample_uuid, result_type, data, dryrun=dryrun)
            except Exception as exception:  # pylint:disable=broad-except
                result['type'] = 'error'
                result['exception'] = str(exception)
            return result
        return try_upload

    def upload_all_results(self, group_uuid, samples, dryrun=True):
        """Upload all samples and results to group."""
        executor = ThreadPoolExecutor(max_workers=5)
        results = []
        for sample_name, tool_results in samples.items():
            print(f'[uploader {datetime.now()}] creating sample {sample_name}', file=stderr)
            sample_uuid = self.create_sample(sample_name, group_uuid)
            futures = []
            for tool_result in tool_results:
                result = {
                    'type': 'success',
                    'sample_uuid': sample_uuid,
                    'sample_name': sample_name,
                    'result_type': tool_result['result_type'],
                }
                try_upload = self.get_try_upload(
                    sample_uuid,
                    sample_name,
                    tool_result['result_type'],
                    result,
                    tool_result['data'],
                    dryrun
                )
                futures.append(executor.submit(try_upload))

            for future in futures:
                result = future.result()
                results.append(result)

        return results
