# Makefile for common `sdep` development tasks.

# DOCKER_IMAGE is the name of the docker image we use for development.
DOCKER_IMAGE=mattjmcnaughton/sdep-dev

# DOCKER_RUN is the prefix for any `local` command we want to run in the Docker
# environment. Using `python:3-onbuild` means that when built our image will
# copy in `requirements.txt` and run `pip install` before copying the current
# directory into `/usr/src/app`.
DOCKER_RUN:=docker run -it --rm -v $(shell pwd):/sdep mattjmcnaughton/sdep-dev

# Build the docker image for local use.
build_docker:
	docker build -t $(DOCKER_IMAGE) .

# Test the application.
local_test:
	nose2

# Test the application in the Docker environment.
test:
	$(DOCKER_RUN) /bin/bash -c "make local_test"

# Lint the application.
local_lint:
	pylint ./sdep

# Lint the application in the Docker environment.
lint:
	$(DOCKER_RUN) /bin/bash -c "make local_lint"

# Push the package to pypi.
push:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

# Release a new version of the application.
# Updates the version number, commits with the updated version number, tags and
# pushes to Github, builds and pushes documentation, and then pushes the new version to pypi.
release:
	echo "@TODO"
