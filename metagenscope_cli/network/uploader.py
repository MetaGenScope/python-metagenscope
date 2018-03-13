from metagenscope_cli.config import config
from .token_auth import TokenAuth
import requests
from datetime import datetime


class UploadAuthenticationError(Exception):
    pass


class Uploader:

    def __init__(self, url, headers=None, auth=None):
        self.url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {'Accept': 'application/json'}

        self.auth_warn = None
        if auth is None:
            try:
                auth = config.get_token()
                self.auth = TokenAuth(auth)
            except KeyError:  # no stored token
                self.auth_warn = 'no_auth'
        else:
            self.auth = TokenAuth(auth)
            self.auth_warn = 'unknown_token'

        self.sample_uuid_map = None

    def warnings(self):
        return self.auth_warn

    def supress_warnings(self):
        self.auth_warn = None

    def _cache_sample_uuid(self, sample_name, sample_uuid):
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        self.sample_uuid_map[sample_name] = sample_uuid

    def _cache_sample_uuids(self):
        assert False

    def _get_sample_uuid(self, sample_name, strict=False):
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        try:
            return self.sample_uuid_map[sample_name]
        except KeyError:
            if strict:
                raise
            return sample_name

    def _upload_payload(self, endpoint, payload):
        if self.auth_warn is not None:
            raise UploadAuthenticationError(self.auth_warn)
        response = requests.post(self.url,
                                 headers=self.headers,
                                 auth=self.auth,
                                 json=payload)
        response.raise_for_status()
        return response

    def _create_upload_group(self):
        curtime = datetime.now().isoformat()
        upload_group_name = 'upload_group_{}'.format(curtime)
        response = self.create_sample_group(upload_group_name)
        self.upload_group_id = response['uuid']
        return self.upload_group_id

    def upload_sample_result(self, sample_name,
                             result_name, result_type, data):
        sample_uuid = self._get_sample_uuid(sample_name, strict=True)
        payload = {
            'result_name': result_name,
            'tool_name': result_type,
            'data': data,
        }
        endpoint = f'/api/v1/samples/{sample_uuid}/{result_type}'
        return self._upload_payload(endpoint, payload)

    def create_sample(self, sample_name, group_id=None, metadata={}):
        if group_id is None:
            self._create_upload_group()
            group_id = self.upload_group_id
        payload = {
            "sample_group_uuid": group_id,
            "name": sample_name,
            "metadata": metadata
        }
        response = self._upload_payload('/api/v1/samples', payload)
        sample_uuid = response['uuid']
        self._cache_sample_uuid(sample_name, sample_uuid)
        return response

    def create_sample_group(self, group_name):
        payload = {"name": group_name}
        response = self._upload_payload('/api/v1/sample_groups', payload)
        return response
