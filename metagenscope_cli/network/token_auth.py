"""MetaGenScope API Token auth model."""

from requests.auth import AuthBase

from metagenscope_cli.config import config


class TokenAuth(AuthBase):  # pylint: disable=too-few-public-methods
    """Attaches MetaGenScope Token Authentication to the given Request object."""

    def __init__(self, jwt_token=None):
        """Create TokenAuth from JWT, if provided, or from config file otherwise."""
        self.jwt_token = jwt_token

        if self.jwt_token is None:
            try:
                self.jwt_token = config.get_token()
            except KeyError:
                # No saved token
                raise

    def __call__(self, request):
        """Add authentication header to request."""
        request.headers['Authorization'] = f'Bearer {self.jwt_token}'
        return request

    def __str__(self):
        """Return string representation of TokenAuth."""
        return self.jwt_token
