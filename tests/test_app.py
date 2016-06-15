"""
Tests for `app.py`, particularly the `Sdep` class.
"""

# pylint: disable=import-error

import os
import shutil
import tempfile
import unittest

from collections import namedtuple

import boto3

from moto import mock_s3

from sdep.app import Sdep
from sdep.config import Config

class SdepTestCase(unittest.TestCase):
    """
    Test cases for the `Sdep` class.
    """

    # UploadInfo is a helper named tuple making it easier to return information
    # from `SdepTestCase#_create_test_upload_dir`. It is defined within the
    # `SdepTestCase` class because it will never be used externally.
    UploadInfo = namedtuple("UploadInfo", "tmp_dir num_files created_keys")

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        self._sdep = Sdep(config=Config(test_mode=True))
        self._s3_client = boto3.client("s3", aws_access_key_id="TEST_ID",
                                       aws_secret_access_key="TEST_KEY")

    @mock_s3
    def test_create(self):
        """
        For now, we do not test this method because we test of the individual
        components, and the individual components do not interact at all.
        """
        pass

    @mock_s3
    def test_upload(self):
        """
        Like `test_create`, we do not test the `upload` method because we test
        the individual components.
        """
        pass

    @mock_s3
    def test_create_s3_buckets(self):
        """
        Test that creating s3 buckets works successfully.
        """
        self._sdep.create_s3_buckets()

        # Confirm that we created the single bucket for storing our website.
        # This test will become more complicated once we have the option of also
        # creating a `www` subdomain bucket and a `logs` bucket.
        resp_buckets = self._s3_client.list_buckets()["Buckets"]
        self.assertEqual(1, len(resp_buckets))

        bucket = resp_buckets[0]
        bucket_name = self._sdep.aws_naming()[Sdep.BUCKET_NAME]
        self.assertEqual(bucket["Name"], bucket_name)

        # Confirm that our bucket has the proper usage policy.
        resp = self._s3_client.get_bucket_policy(Bucket=bucket_name)
        self.assertTrue(len(resp["Policy"]) > 0)

    @mock_s3
    def test_upload_files_to_s3(self):
        """
        Test uploading test files to s3 works successfully.

        We create (and then delete) tmp directory containing two files (one
        should be nested in a directory), which we upload tos3. We then check
        that two files have been uploaded to the bucket.
        """
        # Setup by first creating the bucket (we must do this because every test
        # has a new `@mock_s3` environment).
        self._sdep.create_s3_buckets()

        upload_info = self._create_test_upload_dir()
        self._sdep.config.put(Config.SITE_DIR_FIELD, upload_info.tmp_dir)

        self._sdep.upload_files_to_s3()

        bucket_name = self._sdep.aws_naming()[Sdep.BUCKET_NAME]
        resp_objects = self._s3_client.list_objects(Bucket=bucket_name)
        contents = resp_objects["Contents"]

        self.assertEqual(len(contents), upload_info.num_files)

        returned_keys = [c["Key"] for c in contents]
        for key in upload_info.created_keys:
            self.assertTrue(key in returned_keys)

        shutil.rmtree(upload_info.tmp_dir, ignore_errors=True)

    @mock_s3
    def test_configure_bucket_website(self):
        """
        Test configuring the bucket to work as a website works successfully.
        """
        self._sdep.create_s3_buckets()
        self._sdep.configure_bucket_as_website()

        bucket_name = self._sdep.aws_naming()[Sdep.BUCKET_NAME]

        # @TODO Again we will need to update this once we make
        # `IndexDocument#Suffix` and `ErrorDocument#Key` optionally configurable
        # with `Config`.
        resp = self._s3_client.get_bucket_website(Bucket=bucket_name)

        self.assertNotEqual(resp["IndexDocument"]["Suffix"], None)
        self.assertNotEqual(resp["ErrorDocument"]["Key"], None)

    def test_predict_content_type(self):
        """
        There are some strange edge cases having to do with the setting the
        `ContentType` metadata for files, so we perform some tests just to make
        sure our module is working as expected.
        """
        poss_keys = [
            "index.html",
            "pic.jpg",
            "style.css",
            "main.js",
            "fontawesome/fonts/fontawesome-webfont.eot",
            "fontawesome/fonts/fontawesome-webfont.woff",
            "fontawesome/fonts/fontawesome-webfont.woff2",
            "fontawesome/fonts/FontAwesome.otf",
            "fontawesome/fonts/fontawesome-webfont.ttf"
        ]

        for key in poss_keys:
            self.assertNotEqual(Sdep.predict_content_type(key), None)

    @classmethod
    def _create_test_upload_dir(cls):
        """
        Create a temporary directory simulating the directory containing the
        static files for a website.

        Returns:
            UploadInfo: A named tuple containing the path to the temp directory, the
            number of files we created, and names of the files (keys) we expect
            to be uploaded.
        """
        dir_name = tempfile.mkdtemp()
        subdir_name = os.path.join(dir_name, "public")

        os.makedirs(subdir_name)

        index_file = os.path.join(dir_name, "index.html")
        js_file = os.path.join(subdir_name, "index.js")

        created_files = [index_file, js_file]

        for file_to_write in created_files:
            with open(file_to_write, "w+") as test_file:
                test_file.write("TEST")

        return cls.UploadInfo(tmp_dir=dir_name, num_files=len(created_files),
                              created_keys=["index.html", "public/index.js"])
