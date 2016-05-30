"""
Tests for the `config`.
"""

# pylint: disable=import-error

import os
import shutil
import tempfile
import unittest
import uuid

from collections import namedtuple

import simplejson as json

from mock import patch

from sdep.config import Config, ConfigParseError

class ConfigTestCase(unittest.TestCase):
    """
    Test cases for the `Config` class.
    """

    # MockDirs is a helper named tuple making it easier to return the temporary
    # dirs with which we will mock `current` and `home` dir.
    MockDirs = namedtuple("MockDirs", "current home")

    def test_load_config_from_file(self):
        """
        Test that we properly read in the configuration when it is specified
        through a file.
        """
        config_file = self._create_config_file()
        config = Config(config_file=config_file)

        for field in Config.required_config_fields():
            self.assertNotEqual(config.get(field), None)

        os.remove(config_file)

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
        temp_dirs = self._create_mock_dirs()

        with patch('os.getcwd', return_value=temp_dirs.current):
            with patch('os.path.expanduser', return_value=temp_dirs.home):
                config_in_curr = os.path.join(os.getcwd(),
                                              Config.DEFAULT_CONFIG_FILE_NAME)
                self._create_config_file(config_in_curr)

                config = Config()

                self.assertEqual(config_in_curr, Config.locate_config_file())
                for field in Config.required_config_fields():
                    self.assertNotEqual(config.get(field), None)

        for temp_dir in [temp_dirs.current, temp_dirs.home]:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_find_config_in_home_dir(self):
        """
        Test that we locate the configuration file when it is not explicitly
        specified in the command line, but rather located in the users home
        dir.
        """
        # @TODO Is there too much overlap between this method and
        # `test_find_config_in_home_dir`?

        temp_dirs = self._create_mock_dirs()

        with patch('os.getcwd', return_value=temp_dirs.current):
            with patch('os.path.expanduser', return_value=temp_dirs.home):
                config_in_home = os.path.join(os.path.expanduser("~"),
                                              Config.DEFAULT_CONFIG_FILE_NAME)
                self._create_config_file(config_in_home)

                config = Config()

                self.assertEqual(config_in_home, Config.locate_config_file())
                for field in Config.required_config_fields():
                    self.assertNotEqual(config.get(field), None)

        for temp_dir in [temp_dirs.current, temp_dirs.home]:
            shutil.rmtree(temp_dir, ignore_errors=True)


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

    @classmethod
    def _create_mock_dirs(cls):
        """
        A helper method to create two separate temporary directories which we
        will use to mock the current and home directory respectively. Using this
        method, in conjunction with mocking, allows us to completely isolate our
        test suite from the user's local filesystem.

        Returns:
            MockDirs: The locations of the mock directories.
        """
        temp_current = tempfile.mkdtemp()
        temp_home = tempfile.mkdtemp()

        return cls.MockDirs(current=temp_current, home=temp_home)

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
