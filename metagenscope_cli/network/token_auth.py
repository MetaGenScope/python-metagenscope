"""MetaGenScope API Token auth model."""

from requests.auth import AuthBase


# pylint: disable=too-few-public-methods
class TokenAuth(AuthBase):
    """Attaches MetaGenScope Token Authentication to the given Request object."""

    def __init__(self, token):
        """Create TokenAuth for an API Token."""
        self.token = token

    def __call__(self, request):
        """Add authentication header to request."""
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request

    def __str__(self):
        return self.token
