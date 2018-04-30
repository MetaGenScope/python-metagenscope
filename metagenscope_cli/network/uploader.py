"""Uploader class handles uploading samples to a server."""

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
        response = self.knex.post('/api/v1/samples', payload)
        sample_uuid = response['data']['sample']['uuid']
        return sample_uuid

    def upload_sample_result(self, sample_uuid, result_type, data):
        """Upload a tool result of specified type to existing sample."""
        endpoint = f'/api/v1/samples/{sample_uuid}/{result_type}'
        response = self.knex.post(endpoint, data)
        return response

    def upload_all_results(self, group_uuid, samples):
        """Upload all samples and results to group."""
        # TODO: How should this handle failures at each step? Raise if create_sample,
        #       then just catch and collect tool result errors to warn user about?
        results = []
        for sample_name, tool_results in samples.items():
            # TODO: source metadata? Maybe from DataSuper but not files?
            sample_uuid = self.create_sample(sample_name, group_uuid)

            for tool_result in tool_results:
                result_type = tool_result['result_type']
                data = tool_result['data']
                result = {
                    'type': 'success',
                    'sample_uuid': sample_uuid,
                    'sample_name': sample_name,
                    'result_type': result_type,
                }
                try:
                    self.upload_sample_result(sample_uuid, result_type, data)
                except Exception as exception:  # pylint:disable=broad-except
                    result['type'] = 'error'
                    result['exception'] = str(exception)
                results.append(result)
        return results
