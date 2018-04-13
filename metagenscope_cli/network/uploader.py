from datetime import datetime
from .knex import Knex
import json


def json_head(obj, n=5):
    if type(obj) == dict:
        out = {}
        for k, v in obj.items():
            if len(out) == n:
                break
            out[k] = json_head(v, n=n)
    elif type(obj) == list:
        out = []
        for v in obj:
            if len(out) == n:
                break
            out.append(json_head(v, n=n))
    else:
        return obj
    return out


class Uploader:

    def __init__(self, url, headers=None, auth=None):
        self.knex = Knex(url, headers=headers, auth=auth)
        self.sample_uuid_map = None
        self.upload_group_id = None

    def warnings(self):
        return self.knex.warnings()

    def suppress_warnings(self):
        self.knex.suppress_warnings()
        return self

    def _cache_sample_uuid(self, sample_name, sample_uuid):
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        self.sample_uuid_map[sample_name] = sample_uuid

    def _cache_sample_uuids(self):
        self.sample_uuid_map = {}

    def _get_sample_uuid(self, sample_name, strict=False):
        if self.sample_uuid_map is None:
            self._cache_sample_uuids()
        try:
            return self.sample_uuid_map[sample_name]
        except KeyError:
            if strict:
                raise
            return sample_name

    def _create_upload_group(self):
        if self.upload_group_id is not None:
            return self.upload_group_id
        curtime = datetime.now().isoformat()
        upload_group_name = 'upload_group_{}'.format(curtime)
        response = self.create_sample_group(upload_group_name)
        self.upload_group_id = response.json()['data']['sample_group']['uuid']
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
        return self.knex.upload_payload(endpoint, payload)

    def create_sample(self, sample_name, group_id=None, metadata={}):
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
        payload = {"name": group_name}
        response = self.knex.upload_payload('/api/v1/sample_groups', payload)
        return response
