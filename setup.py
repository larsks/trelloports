#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = 'trelloports',
    description = 'Generate reports from Trello boards',
    long_description = open('README.md').read(),
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@oddbit.com',
    version = "1.00",
    packages = find_packages(),
    install_requires = open('requirements.txt').readlines(),
    entry_points = {
        'console_scripts': [
            'trelloport = trelloports.main:main'
            ],
        },
)

