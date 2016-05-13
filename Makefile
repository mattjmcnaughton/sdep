# Makefile for common `sdep` development tasks.

# Push the package to pypi.
push:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

# Release a new version of the application.
# Updates the version number, commits with the updated version number, tags and
# pushes to Github, and then pushes the new version to pypi.
release:
	echo "@TODO"
