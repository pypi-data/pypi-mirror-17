from setuptools import setup

setup(
    name='pbs-generator',
    packages=['pbs_generator'],
    version='0.6',
    install_requires=[
        'Click'
    ],
    description = 'A PBS script generator',
    author = 'Mohamad Mohebifar',
    author_email = 'mmohebifar@mun.ca',
    url = 'https://github.com/mohebifar/pbs-generator',
    download_url = 'https://github.com/mohebifar/pbs-generator/tarball/0.1',
    keywords = ['pbs-generator', 'rowley'],
    classifiers = [],
)
