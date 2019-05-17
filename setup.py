#!/usr/bin/env python3 

from setuptools import setup
from os.path import dirname, abspath, join

base_path = dirname(abspath(__file__))

with open(join(base_path, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup(
    name="vertrag",
    description='Contract creation for westnetz w.V.',
    author='olf42',
    author_email='olf@subsignal.org',
    url='https://github.com/westnetz/vertrag',
    packages=['vertrag'],
    install_requires=requirements,
    version="0.1",
    entry_points="""
        [console_scripts]
        vertrag=vertrag.cli:cli
    """,
)

