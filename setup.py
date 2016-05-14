"""
sdep
----

sdep is a cli for easily deploying a static website using Amazon Web
Services, Cloudfront, and Route 53.
"""

from setuptools import setup

VERSION = '0.1'

setup(
    name='sdep',
    # Automatically read the version from `sdep/__init__.py`.
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
        'click>=6.0'
    ]
)
