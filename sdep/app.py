"""
This file contains the `Sdep` class as well as any related classes and functions
necessary for creating and updating a static website on AWS.
"""

class Sdep(object):
    """
    An instance of this `Sdep` class is responsible for defining all actions
    which can be taken on the specified static website.

    Args:
        config (Config): The configuration to use for this specific action.

    Returns:
        sdep: An instance of the `Sdep` class.
    """

    def __init__(self, config):
        self._config = config

    def create(self):
        """
        Perform the initial creation of the static website on AWS. This command
        will perform the following actions:
        - Perform the initial upload of the static files.
        """
        pass

    def update(self):
        """
        Update the static website on AWS. This will perform the following
        actions:
        - Update static files that have changed.
        """
        pass
