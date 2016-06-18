.. _example:

Quickstart Example
==================

.. versionadded:: 0.1.0

The following example demonstrates using **sdep** to create a static website. In
addition to **sdep**, and Amazon S3, we utilize `travis-ci
<https://travis-ci.org/>`_, `Cloudflare <https://www.cloudflare.com/>`_, and an
external DNS provider of your choice (I'm a fan of `hover
<https://www.hover.com/>`_).

Creating Accounts
-----------------

Before we begin, sign up for the following accounts if you do not have them
already: Github, travis-ci, Amazon Web Services, Cloudflare, and a DNS provider
of your choice.

Initial Upload and Configuration
--------------------------------

To start, we assume that you've purchased a domain name from some DNS provider.

AWS
~~~

- From AWS' IAM service page, create a new :command:`AWS_ACCESS_KEY_ID` and
  :command:`AWS_SECRET_ACCESS_KEY` for your user, through using your user's
  **Security Credentials** tab. This user must have access to S3.
    - Store these credentials, as we will need them later.

Sdep
~~~~

- Assuming you have python3 and pip installed, download **sdep** with
  :command:`pip install sdep`.
- Run the following command::

    export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID;
    export AWS_SECRET_ACCESS_KEY=YOUR_AWS_ACCESS_KEY;
    export SITE_DIR=PATH_TO_SITE_YOU_WISH_TO_DEPLOY;
    export DOMAIN=YOUR_DOMAIN; sdep create

:command:`AWS_ACCESS_KEY_ID` and :command:`AWS_SECRET_ACCESS_KEY` are the
credentials from the **AWS** step. :command:`SITE_DIR` is the directory
containing your static website (ex. the :command:`./public` directory in a
static website built by `hugo <https://gohugo.io/>`_), and :command:`DOMAIN` is
the domain name you purchased.

Your website is now deployed on S3, and can be accessed by accessing its
endpoint (ex.
:command:`http://mattjmcnaughton.com.s3-website-us-east-1.amazonaws.com`).
Throughout the rest of the tutorial, we'll refer to this as
:command:`S3_ENDPOINT`, and it can be found through going to **Properties** tab
of the S3 bucket representing your website, and then going to the **Static
Website Hosting** section.

Cloudflare
~~~~~~~~~~

- From the account overview page, click **Add Site**.
    - Enter the domain name you have purchased (ex. "mattjmcnaughton.com") and
      click **Continue Setup**.
- Delete the :command:`A Record` with :command:`YOUR_DOMAIN_NAME`. Add a new
  :command:`CNAME` with :command:`Name` equal to :command:`YOUR_DOMAIN_NAME`
  (i.e. mattjmcnaughton.com) and :command:`DOMAIN_NAME` equal to
  :command:`S3_ENDPOINT`.
    - After creating, click the Cloud with the Arrow throughout so that it becomes
      Orange.
- Click continue, and then select the Free Website plan.
- Record the Nameservers shown by Cloudflare. We will need them later to update
  our DNS provider.

If you want SSL:

- Go to the **Crypto** Tab and ensure **SSL** is set to :command:`Flexible`.
- Go to the **Page Rules** Tab and change turn on the **Always Use HTTPS** page
  rule.

DNS Provider
~~~~~~~~~~~~

- Delete any previous A or CNAME records on your DNS provider.
- Configure the Nameservers on your DNS provider to be the Cloudflare's
  Nameservers.

Continuous Deployment
---------------------

If you are happy with manually deploying your static website, then congrats,
you're done! Simply replace :command:`sdep create` with :command:`sdep update`
whenever you make a change.

However, using a continuous integration build tool like `travis-ci
<https://travis-ci.org>`_, it is possible to deploy your static site to S3
anytime a pull request is merged.

Assuming your Github account is linked with travis-ci, and your static website
is hosted on Github, take the following steps:

- Turn on travis-ci for this repo.
- Go to settings and turn off **Build Pull Requests**, but ensure that **Build
  Pushes** is turned on.

Then in the root directory of the repository containing your application, create
a :command:`.travis.yml` file with the following contents::

    language: go
    install: go get -v github.com/spf13/hugo
    sudo: required
    script:
    - hugo -v
    - sudo pip install sdep>=0.1.0
    - sdep update
    branches:
      only:
      - master
    env:
      global:
      - SITE_DIR=YOUR_SITE_DIR
      - DOMAIN=YOUR_DOMAIN

Then, from the command line run :command:`travis encrypt
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY --add env.global` and :command:`travis
encrypt AWS_SECRET_ACCESS_KEY --add env.global`. You will need to run
:command:`gem install travis` if you do not have the `travis-ci gem
<https://rubygems.org/gems/travis/versions/1.8.2>`_ installed.

Then, just push to Github. Anytime you merge a pull request, **sdep** will
deploy your website once again.

You're Done!
------------

Success, you did it! Looking for next steps, we'd love any `contributions
<https://github.com/mattjmcnaughton/sdep/blob/master/CONTRIBUTING.md>`_. If you
encountered any issues going through this tutorial, please let us know `here
<https://github.com/mattjmcnaughton/sdep/issues>`_. We'd love to try and help
you out!
