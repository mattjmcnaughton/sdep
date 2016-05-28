"""
This file contains the `Sdep` class as well as any related classes and functions
necessary for creating and updating a static website on AWS.
"""

# pylint: disable=import-error

import os

import boto3

import simplejson as json

from .config import Config

class Sdep(object):
    """
    An instance of this `Sdep` class is responsible for defining all actions
    which can be taken on the specified static website.

    Args:
        config (Config): The configuration to use for this specific action.

    Returns:
        sdep: An instance of the `Sdep` class.
    """

    # Constant names of AWS objects.
    BUCKET_NAME = "bucket_name"

    # Default index and error.
    # @TODO This specification is temporary, as eventually we will make these
    # configurable options with `Config`.
    DEFAULT_INDEX_SUFFIX = "index.html"
    DEFAULT_ERROR_KEY = "404.html"

    def __init__(self, config):
        self._config = config
        self._s3_client = self._establish_s3_client()

    @property
    def config(self):
        """
        Read only access of this instance's `Config` instance.

        We make this publicly accessible because often during testing we need to
        update configuration values on the fly (mostly for inserting the name of
        test directories).

        @TODO Would it be better to do this through just mocking individual
        calls?

        Returns:
            Config: The configuration for this file.
        """
        return self._config

    def _establish_s3_client(self):
        """
        Return a boto3 client connected to s3 with the configured auth tokens.

        Returns:
            S3.Client: The client we use to communicate with s3.
        """
        # We will not even be attempting to create an instance of the `Sdep`
        # class, unless these values exist, so we are confident they do.
        access_key = self.config.get(Config.AWS_ACCESS_KEY_ID_FIELD)
        secret_key = self.config.get(Config.AWS_SECRET_ACCESS_KEY_FIELD)

        return boto3.client("s3", aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key)

    def create(self):
        """
        Perform the initial creation of the static website on AWS. This command
        will perform the following actions:
        - Create the s3 buckets with the proper permissions.
        - Upload all of the files.
        - Configure the s3 bucket to serve as a website.
        """
        self.create_s3_buckets()
        self.upload_files_to_s3()
        self.configure_bucket_as_website()

    def create_s3_buckets(self):
        """
        Create the buckets in which we will place the static content.

        AWS specifies that we must name the bucket the same name as our domain.
        """
        bucket_name = self._bucket_name()

        self._s3_client.create_bucket(Bucket=bucket_name)
        self._s3_client.put_bucket_policy(
            Bucket=bucket_name, Policy=self._public_bucket_policy(bucket_name))

        # @TODO
        # This is where we will perform the check to see if we should also
        # create a `www.` subdomain bucket in addition to check if the
        # configuration specifies a region.

        # @TODO This is where we will optionally configure logging (which would
        # require the creation of additional buckets).

    def upload_files_to_s3(self):
        """
        Upload every file from the static website directory to s3.
        """
        site_dir = self.config.get(Config.SITE_DIR_FIELD)

        for path, _, files in os.walk(site_dir):
            for file_name in files:
                full_path = os.path.join(path, file_name)

                # We want the key name to be the full path, assuming we treat
                # `site_dir` as the root. We add `+ 1` to cut off a `/`.
                key_name = full_path[len(site_dir) + 1:]

                self._s3_client.upload_file(full_path, self._bucket_name(),
                                            key_name)

    def configure_bucket_as_website(self):
        """
        For a bucket to serve as a static website, AWS requires some specific
        configuration.
        """
        self._s3_client.put_bucket_website(
            Bucket=self._bucket_name(),
            WebsiteConfiguration=self._website_config()
        )

    def aws_naming(self):
        """
        Many of our methods for generating the names that we use for AWS objects
        (like buckets) are private, which makes sense. However, often in tests
        we need to access these names. As such, this method returns a hash of
        all AWS specific names. The implementation of this method means we can
        access the information while keeping private methods private.

        Returns:
            dict: A dictionary of the names of aws objects.
        """
        return {self.BUCKET_NAME: self._bucket_name()}


    def _bucket_name(self):
        """
        The name of the bucket we use for hosting our static site.

        Returns:
            str: The bucket name.
        """
        return self.config.get(Config.DOMAIN_FIELD)

    @staticmethod
    def _public_bucket_policy(bucket_name):
        """
        A helper method for getting a bucket policy which allows anyone to view
        our static website.

        Args:
            bucket_name (str): The bucket for which we are creating the policy.

        Returns:
            str: A json dump of the policy.
        """

        json_policy = {
            "Version":"2012-10-17",
            "Statement": [{
                "Sid": "Allow Public Access to All Objects",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::{0}/*".format(bucket_name)
            }]
        }

        return json.dumps(json_policy)

    def _website_config(self):
        """
        Helper method returning the configuration for the api call to transform
        our bucket into a website.

        Returns:
            dict: Configuration stored within a dictionary.
        """
        website_config = {
            "IndexDocument": {
                "Suffix": self.DEFAULT_INDEX_SUFFIX
            },
            "ErrorDocument": {
                "Key": self.DEFAULT_ERROR_KEY
            }
        }

        return website_config

    def update(self):
        """
        Update the static website on AWS. This will perform the following
        actions:
        - Update static files that have changed.
        """
        pass
