"""
This file contains the `Configuration` class as well as related classes
necessary for controlling `sdep` configuration.
"""

# pylint: disable=import-error

import os
import simplejson as json

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

    # Unless otherwise specified, we assume the config file is named `.sdeprc`.
    DEFAULT_CONFIG_FILE_NAME = ".sdeprc"

    def __init__(self, config_file=None):
        self._config_hash = {}

        if config_file is None or not os.path.isfile(config_file):
            config_file = self._locate_config_file()
        else:
            config_file = os.path.join(os.getcwd(), config_file)

        try:
            if config_file is None:
                self._parse_from_env()
            else:
                self._parse_from_config_file(config_file)

        except (ConfigFileDoesNotExistError, ConfigImproperFormatError):
            raise ConfigParseError

    def get(self, field):
        """
        Get a configuration value for the specified field. This is the ONLY way
        we should be inquiring about configuration values.

        Args:
            field (str): The field for which we want the configuration value.

        Returns:
            str: The value for the specified field or `None` if the value has no
            specified configuration.
        """
        return self._config_hash.get(field)

    @classmethod
    def _locate_config_file(cls):
        """
        Determine if a configuration file exists either in the current directory
        or the home directory.

        Returns:
            str: The path to the configuration file or `None` if no path is
                specified.
        """
        curr_dir_file = os.path.join(os.getcwd(), cls.DEFAULT_CONFIG_FILE_NAME)
        home_dir_file = os.path.join(os.path.expanduser("~"),
                                     cls.DEFAULT_CONFIG_FILE_NAME)

        for poss_config_file in [curr_dir_file, home_dir_file]:
            if os.path.isfile(poss_config_file):
                return poss_config_file

        return None

    def _parse_from_env(self):
        """
        Fill in the instance of `Config` with the information contained in the
        environment variables.

        Raises:
            ConfigImproperFormatError: If vital configuration data is either in
                the incorrect format or nonexistent.
        """
        for field in self._required_config_fields(env=True):
            value = os.environ.get(field)

            if value is None:
                raise ConfigImproperFormatError
            else:
                self._config_hash[value.lower()] = value

    def _parse_from_config_file(self, config_file):
        """
        Fill in the instance of `Config` with the information contained in
        `config_file`. The configuration file MUST be in JSON format.

        Args:
            config_file (str): The path to the configuration file.

        Raises:
            ConfigImproperFormatError: If vital configuration data is either in
                the incorrect format or nonexistent.
        """
        config_data = None

        try:
            with open(config_file) as json_file:
                config_data = json.loads(json_file.read())
        except (IOError, json.JSONDecodeError) as err:
            raise ConfigImproperFormatError(err.message)

        # @TODO Should a common helper method implement this functionality
        # for both `_parse_from_config_file` and `_parse_from_env`.
        for field in self._required_config_fields(env=False):
            value = config_data.get(field)

            if value is None:
                raise ConfigImproperFormatError
            else:
                self._config_hash[value.lower()] = value

    @staticmethod
    def _required_config_fields(env=False):
        """
        Return the required configuration fields either in `snake_case` or in all
        upper-case `snake_case`, depending on whether the `env` flag is set.

        Args:
            env (bool): A boolean flag indicating what capitalization we should
                use when returning the fields.

        Returns:
            [str]: A list of required configuration fields.
        """
        required_fields = [
            "aws_access_key_id", "aws_secret_access_key", "site_dir"
        ]

        if env:
            return [field.upper() for field in required_fields]
        else:
            return required_fields

    @staticmethod
    def _optional_config_fields(env=False):
        """
        Return the optinal configuration fields either in `snake_case` or in all
        upper-case `snake_case`, depending on whether the `env` flag is set.

        Args:
            env (bool): A boolean flag indicating what capitalization we should
                use when returning the fields.

        Returns:
            [str]: A list of optional configuration fields.
        """
        optional_fields = []

        if env:
            return [field.upper() for field in optional_fields]
        else:
            return optional_fields