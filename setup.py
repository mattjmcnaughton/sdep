"""
sdep
----

sdep is a cli for easily deploying a static website using Amazon Web
Services, Cloudfront, and Route 53.
"""

from distutils.core import setup

version = '0.1'

setup(
    name='sdep',
    # Automatically read the version from `sdep/__init__.py`.
    version=version,
    description='A cli for easily deploying static websites',
    author='Matt McNaughton',
    license='MIT',
    author_email='mattjmcnaughton@gmail.com',
    url='https://github.com/mattjmcnaughton/sdep',
    # Make sure to tag releases appropriately.
    download_url="https://github.com/mattjmcnaughton/sdep/tarball/{0}".format(version),
    keywords=['deployments', 'cli'],
    # Include the dependencies with version numbers.
    install_requires=[],
    entry_points='''
        sdep=sdep.cli:main
    '''
)
