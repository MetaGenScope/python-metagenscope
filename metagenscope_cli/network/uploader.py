from metagenscope_cli.config import config
from .token_auth import TokenAuth
import requests


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

    def warnings(self):
        return self.auth_warn

    def supress_warnings(self):
        self.auth_warn = None

    def upload_data(self, result_name, result_type, data):
        payload = {
            'result_name': result_name,
            'tool_name': result_type,
            'data': data,
        }
        return self.upload_payload(payload)

    def upload_payload(self, payload):
        if self.auth_warn is not None:
            raise UploadAuthenticationError(self.auth_warn)
        request = requests.post(self.url,
                                headers=self.headers,
                                auth=self.auth,
                                json=payload)
        return request

    def create_sample(self, sample_name, result_names=[]):
        assert False

    def create_sample_group(self,
                            group_name,
                            subgroups=[],
                            sample_names=[],
                            result_names=[]):
        assert False
