#!/usr/bin/env python

"""
A helper script for running `sdep` directly from the source tree, as if we
downloaded `sdep` with `pip install sdep` and then run `sdep` from the command
line.

Make sure the user has permission to execute with `chmod u+x sdep-runner.py`.
"""

# pylint: disable=invalid-name

from sdep.cli import main

if __name__ == "__main__":
    main()
