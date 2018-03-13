from metagenscope_cli.config import config
from .token_auth import TokenAuth
import requests


class ServerAuthenticationError(Exception):
    pass


class Knex:

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
                self.auth = None
        else:
            self.auth = TokenAuth(auth)
            self.auth_warn = 'unknown_token'

    def warnings(self):
        return self.auth_warn

    def suppress_warnings(self):
        self.auth_warn = None
        return self

    def upload_payload(self, endpoint, payload):
        if self.auth_warn is not None:
            raise ServerAuthenticationError(self.auth_warn)
        url = self.url + endpoint
        response = requests.post(url,
                                 headers=self.headers,
                                 auth=self.auth,
                                 json=payload)
        response.raise_for_status()
        return response

    def get(self, endpoint):
        if self.auth_warn is not None:
            raise ServerAuthenticationError(self.auth_warn)
        url = self.url + endpoint
        response = requests.get(url,
                                 headers=self.headers,
                                 auth=self.auth)
        response.raise_for_status()
        return response
