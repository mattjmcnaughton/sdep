# sdep

**In Progress**

A lightweight tool for continuously deploying static websites using Amazon S3,
Cloudfront, and Route 53.

## Usage

**TBD** - but will include specifying some type of config file and one of the two
actions below.

## Actions

**sdep** defines two actions: `create` and `update`.

- `create` runs the first time the static website is ever created, and is
  responsible for one-time initialization actions such as allocating an IP
  address on Route 53.
- `update` runs every time the static website updates. At the very least, it
  uploads the files to serve to S3 and clears the Cloudfront cache. This actions
  is intended to be run from a continuous integration server such as
  [travis-ci](https://travis-ci.org/) or [Jenkins](https://jenkins.io/).

