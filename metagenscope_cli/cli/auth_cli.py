"""CLI to login, register and authenticate."""

import os
import click
from requests.exceptions import HTTPError

from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.config import config

from .utils import add_authorization


def handle_auth_request(request_generator):
    """Perform common authentication request functions."""
    try:
        jwt_token = request_generator()
        click.echo(f'JWT Token: {jwt_token}')

        if click.confirm('Store token for future use (overwrites existing)?'):
            config.set_token(jwt_token)
    except HTTPError as http_error:
        click.echo(f'There was an error with registration: {http_error}', err=True)


@click.command()
@click.option('-h', '--host', default=None)
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(host, username, user_email, password):
    """Register as a new MetaGenScope user."""
    if host is None:
        host = os.environ['MGS_HOST']
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.register(username, user_email, password)

    handle_auth_request(request_generator)


@click.command()
@click.option('-h', '--host', default=None)
@click.argument('user_email')
@click.argument('password')
def login(host, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    if host is None:
        host = os.environ['MGS_HOST']
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.login(user_email, password)

    handle_auth_request(request_generator)


@click.command()
@add_authorization()
def status(uploader):
    """Get user status."""
    response = uploader.knex.get('/api/v1/auth/status')
    click.echo(response)
