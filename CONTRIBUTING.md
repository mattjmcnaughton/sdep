## Contributing

**sdep** loves contributions! Contributing to the **sdep** can occur
in a number of ways!

## Docker

For developer ease of use, we package the development environment in a Docker
container. There are a ton of great tutorials online about getting Docker up and
running on whatever type of machine you have. If this is your first time working
on `sdep`, run `make build_docker` to build the Docker container we'll use for
the rest of said development tasks.

## Issue Reporting

Please report any issues in the [issue
tracker](https://github.com/mattjmcnaughton/sdep/issues). When reporting an
issue, please follow these guidelines.
- Check the issue has not already been reported.
- Open an issue with a descriptive title and summary.
  - Be as clear, concise, and precise as possible in describing the problem.

## Pull Requests

If you are interested in contributing code to the **sdep**, hooray!
Please let us know if we can answer any questions/help. We're dedicated to
making **ssdep** a supportive environment for contributing to open source for
individuals of any skill level. Please follow these guidelines, and if you
have any questions, ask!
- Read [this](https://gun.io/blog/how-to-github-fork-branch-and-pull-request/)
  blog post on contributing to open source.
- Fork the project.
- Create a topic/feature branch.
  - Please follow the following naming convention for branch names:
    `FIRSTNAME-description`. So for a branch containing README fixes, I
    would name my branch `matt-readme-fixes`.
- Follow the coding conventions of the rest of the project.
  Specifically, **sdep** utilizes a number of linters.
- Please add tests. Unfortunately, we cannot accept pull
  requests missing tests.
- Make sure the test suite passes and all linters pass.
- Squash all related commits together. Read
  [this](http://mattjmcnaughton.com/post/rebasing-git-commits)
  blog post if you need a guide.
- Write a thorough, descriptive, git commit message following the guidelines
  outlined [here](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
- Open a pull request relating to a single subject with clear title,
  description, and proper grammar.

## Linters, Tests and Documentation
**sdep** utilizes `pylint`. Ensure all `*.py`
files being submitted in your pull request lint cleanly when processed with
`make lint`.

**sdep** utilizes `nose2` for tests, which can be found in the `tests` directory.
Ensure running `make test` from the project root
passes, and all new code includes tests.

**sdep** utilizes `docstrings` for documentation. Please document all your code.
Documentation will automatically be updated on
[ReadTheDocs](http://sdep.readthedocs.io) whenever we merge a pr.

Making a pull request will automatically trigger tests and linting using
[Travis CI](https://travis-ci.org/mattjmcnaughton/sdep), and we ask that all pr's
pass tests and static analysis. Basically, if `make test && make lint`
passes, then you should be good to go!
