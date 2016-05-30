"""
sdep
----

sdep is a cli for easily deploying a static website using Amazon Web
Services, Cloudfront, and Route 53.
"""

from setuptools import setup

VERSION = '0.11'

setup(
    name='sdep',
    # @TODO Automatically read the version from `sdep/__init__.py`.
    version=VERSION,
    description='A cli for easily deploying static websites',
    author='Matt McNaughton',
    license='MIT',
    author_email='mattjmcnaughton@gmail.com',
    url='https://github.com/mattjmcnaughton/sdep',
    # Make sure to tag releases appropriately.
    download_url="https://github.com/mattjmcnaughton/sdep/tarball/{0}".format(VERSION),
    keywords=['deployments', 'cli'],
    # Dependencies for `sdep`.
    install_requires=[
        'boto3>=1.0.0',
        'click>=6.0',
        'simplejson>=3.0',
    ],
    # Install `sdep` to the user's site-packages directory.
    packages=["sdep"],
    # Tell pip to generate a script called `sdep` which will invoke
    # `sdep.cli:main`.
    entry_points={
        "console_scripts": ["sdep = sdep.cli:main"]
    }
)
