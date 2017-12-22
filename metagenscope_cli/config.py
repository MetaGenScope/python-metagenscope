"""Interact with configuration file."""
from __future__ import absolute_import

import os.path
import configparser


USER_SECTION_KEY = 'user'
TOKEN_OPTION_KEY = 'token'


class MetagenscopeConfiguration(object):
    """MetaGenScope configuration."""

    def __init__(self, filename, dirname='~'):
        """Load configuration file, if it exists."""
        self.config = configparser.ConfigParser()

        expanded_dirname = os.path.expanduser(dirname)
        self.configuration_filename = os.path.join(expanded_dirname, filename)
        if os.path.isfile(self.configuration_filename):
            self.config.read(self.configuration_filename)

    def get_token(self):
        """Return stored authorization token, if it exists."""
        token = None
        try:
            token = self.config[USER_SECTION_KEY][TOKEN_OPTION_KEY]
        except KeyError:
            pass

        return token

    def set_token(self, new_token):
        """Set and save authorization token."""
        try:
            self.config[USER_SECTION_KEY][TOKEN_OPTION_KEY] = new_token

            with open(self.configuration_filename, 'w') as configfile:
                self.config.write(configfile)
        except KeyError:
            # Create non-existent user section
            self.config[USER_SECTION_KEY] = {}
            self.set_token(new_token)


# pylint: disable=invalid-name
config = MetagenscopeConfiguration('.metagenscope.ini')
