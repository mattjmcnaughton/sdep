.. _cli:

Command Line Interface
======================

.. versionadded:: 0.1

The primary method of running **sdep** is through the command line interface. We use
`click <http://click.pocoo.org/>`_ to easily create a command line interface. It
is through the command line interface that we perform all of the actions
included in **sdep**.

Basic Usage
-----------

After installing **sdep**, you will find a :command:`sdep` script installed.
This script contains the :command:`create` and :command:`update` commands
necessary to deploy a static website from scratch and then update its contents
repeatedly.

We run :command:`create` and :command:`update` as follows::

  sdep (create|update) [--config CONFIG]

create
------

The :command:`create` command should only be run once for each static website.
It does the initial provisioning of Amazon and any other one time tasks.

update
------

The :command:`update` command is run each time the static site changes and needs
to be reployed. It updates any changed static files on Amazon S3, as well as
performing any other deployment updates.

Config
------

The majority of **sdep** commands require the specification of configuration options.
There are two options for specifying this configuration: environment variables and
configuration files.

When we specify variables as environment variables we use all uppercase snake
case (i.e. :command:`AWS_ACCESS_KEY_ID`) and when we specify variables in our configuration
file, we use regular snake case (i.e. :command:`aws_access_key_id`). Furthermore,
certain configuration fields are required, while
other configuration fields are optional. If a configuration field is required,
there is no default value, as **sdep** will terminate if it is not specified. If
a configuration field is optional, a default value is specified. The following
options can be set in configuration files:

**Required**

- :command:`AWS_ACCESS_KEY_ID`: The access key id for one's Amazon Web Services
  account.
- :command:`AWS_SECRET_ACCESS_KEY`: The secret key for one's AWS account.
- :command:`SITE_DIR`: The root directory of the static site.
- :command:`DOMAIN`: The domain name.

**Optional**

- :command:`INDEX_SUFFIX`: When hosting with Amazon S3, it is necessary to
  specify an index suffix, which is appended to all urls ending in :command:`/`. The
  default value is :command:`index.html`.
- :command:`ERROR_KEY`: The S3 key of the file Amazon should serve in case of
  error (i.e. incorrect url). The default value is :command:`404.html`.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Environment variables are a particularly useful configuration option when
using **sdep** on a service such as `travis-ci <https://travis-ci.org>`_ for
which we do not desire to have files containing secrets checked into version
control.

An example of running :command:`update` using environment variables for
configuration is the following::

    export AWS_ACCESS_KEY_ID=MY_ACCESS_KEY_ID; export
    AWS_SECRET_ACCESS_KEY=MY_SECRET_ACCESS_KEY; export SITE_DIR=./static;
    export DOMAIN=sdep-example.com; sdep update

Configuration File
~~~~~~~~~~~~~~~~~~~

It is additionally possible to specify a :command:`.sdeprc` file containing
configuration values. A :command:`.sdeprc` file is just a simple JSON file, as
con be seen below::

    {
      "aws_access_key_id": "MY_ACCESS_KEY_ID",
      "aws_secret_access_key": "MY_SECRET_ACCESS_KEY",
      "site_dir": "./static",
      "domain": "sdep-example.com"
    }

There are three possible ways to specify the location of a :command:`.sdeprc`.
In order of presidence, they are command line flag, specific file in current
directory, and universal file in home directory. Specifying the configuration
file through the command line flag utilizes the :command:`--config` flag, as can
be seen below::

    sdep update --config ./config/.sdeprc

If the :command:`--config` file is not set,
**sdep** will first search for a :command:`.sdeprc` file in the
directory from which we are running the **sdep** command. If no such file
exists, then we will search for a :command:`.sdeprc` file in the user's home
directory. If no such file exists, **sdep** will terminate.
