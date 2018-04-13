"""Uploader class handles uploading samples to a server."""

from datetime import datetime

from .knex import Knex


class Uploader:
    """Uploader class handles uploading samples to a server."""

    def __init__(self, url, headers=None, auth=None):
        """Initialize Uploader instance."""
        self.knex = Knex(url, headers=headers, auth=auth)
        self.sample_uuid_map = None
        self.upload_group_id = None

    def warnings(self):
        """Return network warnings."""
        return self.knex.warnings()

    def suppress_warnings(self):
        """Supress network warnings."""
        self.knex.suppress_warnings()
        return self

    def _cache_sample_uuid(self, sample_name, sample_uuid):
        """Cache UUID for sample."""
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        self.sample_uuid_map[sample_name] = sample_uuid

    def _cache_sample_uuids(self):
        """Reset sample UUID cache."""
        self.sample_uuid_map = {}

    def _get_sample_uuid(self, sample_name, strict=False):
        """Try to hit cache for sample UUID."""
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        try:
            return self.sample_uuid_map[sample_name]
        except KeyError:
            if strict:
                raise
            return sample_name

    def _create_upload_group(self):
        """Create Sample Group for uploading if one does not exist for this session."""
        if self.upload_group_id is not None:
            return self.upload_group_id
        current_time = datetime.now().isoformat()
        upload_group_name = f'upload_group_{current_time}'
        response = self.create_sample_group(upload_group_name)
        self.upload_group_id = response.json()['data']['sample_group']['uuid']
        return self.upload_group_id

    def upload_sample_result(self, sample_name,
                             result_name, result_type, data):
        """Upload a tool result of specified type to existing sample."""
        sample_uuid = self._get_sample_uuid(sample_name, strict=True)
        payload = {
            'result_name': result_name,
            'tool_name': result_type,
            'data': data,
        }
        endpoint = f'/api/v1/samples/{sample_uuid}/{result_type}'
        return self.knex.upload_payload(endpoint, payload)

    def create_sample(self, sample_name, group_id=None, metadata={}):  # pylint: disable=dangerous-default-value
        """Create Sample on remote server."""
        if group_id is None:
            self._create_upload_group()
            group_id = self.upload_group_id
        payload = {
            "sample_group_uuid": group_id,
            "name": sample_name,
            "metadata": metadata
        }
        response = self.knex.upload_payload('/api/v1/samples', payload)
        sample_uuid = response.json()['data']['sample']['uuid']
        self._cache_sample_uuid(sample_name, sample_uuid)
        return response

    def create_sample_group(self, group_name):
        """Create Sample Group on remote server."""
        payload = {"name": group_name}
        response = self.knex.upload_payload('/api/v1/sample_groups', payload)
        return response
