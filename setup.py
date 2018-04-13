# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    package_version = f.read().strip()

setup(
    name='pepp',
    version=package_version,

    description='Simpler pipenv without the virtualenv',
    long_description=long_description,

    url='https://github.com/jeremylow/pepp',

    author='Jeremy Low',
    author_email='jeremy@iseverythingstilltheworst.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='pip',

    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'test_data']),
    install_requires=['toml', 'pipfile', 'click'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)

