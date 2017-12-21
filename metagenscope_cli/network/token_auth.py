"""MetaGenScope API Token auth model."""

from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Attaches MetaGenScope Token Authentication to the given Request object."""

    def __init__(self, token):
        """Create TokenAuth for an API Token."""
        self.token = token

    def __call__(self, request):
        """Add authentication header to request."""
        request.headers['X-API-TOKEN'] = self.token
        return request
