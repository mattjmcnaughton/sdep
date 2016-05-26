"""
Tests for the `config`.
"""

# pylint: disable=import-error

import os
import tempfile
import unittest
import uuid

import simplejson as json

from mock import patch

from sdep.config import Config, ConfigParseError

class ConfigTestCase(unittest.TestCase):
    """
    Test cases for the `Config` class.

    @TODO Overall it would be a big improvement to isolate the file system
    because right now tests may pass/fail based on the location of configuration
    files on users local file systems.
    """

    def test_load_config_from_file(self):
        """
        Test that we properly read in the configuration when it is specified
        through a file.
        """
        config_file = self._create_config_file()
        config = Config(config_file=config_file)

        for field in Config.required_config_fields():
            self.assertNotEqual(config.get(field), None)

        self._cleanup_file(config_file)

    def test_load_config_from_env(self):
        """
        Test that we properly read in the configuration when it is specified in
        environment variables.
        """
        environ_dict = {key.upper(): value for key, value in
                        self._config_dict().items()}

        with patch.dict(os.environ, environ_dict, clear=True):
            config = Config()

            for field in Config.required_config_fields():
                self.assertNotEqual(config.get(field), None)

    def test_find_config_in_curr_dir(self):
        """
        Test that we locate the configuration file when it is not explicitly
        specified in the command line, but rather located in the curr directory
        from which the tests are run.
        """
        curr_dir_loc = os.path.join(os.getcwd(), Config.DEFAULT_CONFIG_FILE_NAME)
        created_file = False

        if not os.path.isfile(curr_dir_loc):
            created_file = True
            self._create_config_file(file_name=curr_dir_loc)

        self.assertNotEqual(Config.locate_config_file(), None)

        if created_file:
            self._cleanup_file(curr_dir_loc)

    def test_find_config_in_home_dir(self):
        """
        Test that we locate the configuration file when it is not explicitly
        specified in the command line, but rather located in the users home
        dir.
        """
        # @TODO Is there too much code duplication between this method and
        # `test_find_config_in_curr_dir`?

        home_dir_loc = os.path.join(os.path.expanduser("~"), Config.DEFAULT_CONFIG_FILE_NAME)
        created_file = False

        if not os.path.isfile(home_dir_loc):
            created_file = True
            self._create_config_file(file_name=home_dir_loc)

        self.assertNotEqual(Config.locate_config_file(), None)

        if created_file:
            self._cleanup_file(home_dir_loc)

    def test_bad_config(self):
        """
        Test loading the configuration from a file with an improperly specified
        configuration.
        """
        config_file = self._create_bad_config_file()

        with self.assertRaises(ConfigParseError):
            Config(config_file=config_file)

    @staticmethod
    def _config_dict():
        """
        A dictionary of property formatted config.

        Returns:
            dict: A properly formatted config.
        """
        return {field: str(uuid.uuid4()) for field in Config.required_config_fields()}

    def _create_config_file(self, file_name=None):
        """
        A helper method to create a demo working configuration file.

        Args:
            file_name(Optional[str]): The location for the desired configuration
                file.

        Returns:
            str: The path to the given configuration file.
        """
        good_config_dict = self._config_dict()

        if file_name is None:
            _, file_name = tempfile.mkstemp()

        with open(file_name, "w+") as new_config_file:
            new_config_file.write(json.dumps(good_config_dict))

        return file_name

    @staticmethod
    def _create_bad_config_file():
        """
        A helper method to create a configuration file that will raise an
        exception when I try to parse it.

        Returns:
            str: The path to the given non-working configuration file.
        """
        _, file_name = tempfile.mkstemp()

        with open(file_name, "w+") as bad_config_file:
            bad_config_file.write(json.dumps({}))

        return file_name

    @staticmethod
    def _cleanup_file(file_path):
        """
        Delete the temporary configuration file we created.

        Args:
            file_path (str): The path to the file we wish to delete.
        """
        os.remove(file_path)
