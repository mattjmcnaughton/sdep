"""
Tests for the `cli`.
"""

# pylint: disable=import-error

import unittest

from click.testing import CliRunner

from sdep.cli import cli

class CliTestCase(unittest.TestCase):
    """
    A collection of test cases for the cli.
    """
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._runner = CliRunner()

    def test_cli_actions_exist(self):
        """
        Test the cli recognizes the actions that should exist.
        """
        actions = ["create", "update"]

        for action in actions:
            result = self._runner.invoke(cli, [action, "--test"])

            self.assertEqual(result.exit_code, 0)
            self.assertTrue(action in result.output)

    def test_cli_actions_not_exist(self):
        """
        Test the cli responds with error code to actions that should not
        exist.
        """
        false_actions = ["delete"]

        for false_action in false_actions:
            result = self._runner.invoke(cli, [false_action, "--test"])

            self.assertNotEqual(result.exit_code, 0)
