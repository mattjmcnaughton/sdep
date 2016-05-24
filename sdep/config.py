"""
This file contains the `Configuration` class as well as related classes
necessary for controlling `sdep` configuration.
"""

import os

class ConfigFileDoesNotExistError(Exception):
    """
    A specialized error we raise when we cannot find a file to use for
    configuration.
    """
    # pylint: disable=too-few-public-methods
    pass

class ConfigImproperFormatError(Exception):
    """
    A specialized error we raise when the user specifies the configuration in an
    improper format.
    """
    # pylint: disable=too-few-public-methods
    pass

class ConfigParseError(Exception):
    """
    A specialized error we raise when for whatever reason we cannot create the
    configuration object.
    """
    # pylint: disable=too-few-public-methods
    pass

class Config(object):
    """
    A class for controlling the configuration of an `sdep` instance.

    Args:
        config_file(Optional[str]): The path to the configuration file used to
            generate the config. If no configuration file is given, then we look
            in the directory from which we are running `sdep` and then the
            user's home directory.

    Returns:
        config: An instance of the `Config` class, filled in with all values
            from either a configuration file or environment variables.

    Raises:
        ConfigParseException: If either configuration does not exist or is
            improperly specified.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, config_file=None):
        try:
            if os.path.isfile(config_file):
                # Parse file.
                pass
            else:
                raise ConfigFileDoesNotExistError

        except (ConfigFileDoesNotExistError, ConfigImproperFormatError):
            raise ConfigParseError
