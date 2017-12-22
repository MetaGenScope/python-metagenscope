import os

import pytest

from metagenscope_cli.config import MetagenscopeConfiguration


def test_get_token(tmpdir):
    """Ensure empty configuration file returns a missing token."""
    test_config = MetagenscopeConfiguration('.metagenscope.ini', str(tmpdir))
    assert test_config.get_token() == None


def test_set_token(tmpdir):
    """Ensure token is written to configuration file correctly."""
    test_config = MetagenscopeConfiguration('.metagenscope.ini', str(tmpdir))
    assert test_config.get_token() == None
    test_config.set_token('foobar')
    assert test_config.get_token() == 'foobar'

    token_present = False
    with open(os.path.join(str(tmpdir), '.metagenscope.ini')) as file:
        for line in iter(file):
            if 'token' in line and 'foobar' in line:
                token_present = True

    assert token_present == True
