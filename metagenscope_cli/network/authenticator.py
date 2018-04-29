"""Handle authentication requests."""

import requests

from metagenscope_cli.constants import DEFAULT_HOST


class Authenticator:
    """Handle authentication requests."""

    def __init__(self, host=None):
        """Initialize Authenticator instance."""
        self.host = host
        if self.host is None:
            self.host = DEFAULT_HOST

    def post_auth(self, endpoint, payload):
        """Post to authentication endpoint, returning JWT token if successful."""
        url = f'{self.host}/api/v1/auth/{endpoint}'
        headers = {'Accept': 'application/json'}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        jwt_token = response.json()['data']['auth_token']

        return jwt_token

    def register(self, username, user_email, password):
        """Perform registration request."""
        payload = {
            'username': username,
            'email': user_email,
            'password': password
        }
        return self.post_auth('register', payload)

    def login(self, user_email, password):
        """Perform login request."""
        payload = {
            'email': user_email,
            'password': password
        }
        return self.post_auth('login', payload)
