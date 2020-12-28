#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from os import path

from tornado_eventsource import __version__

tests_require = [
    'coverage',
    'nose',
    'mock'
]


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tornado_eventsource',
    version=__version__,
    description="EventSource handler for tornado",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='tornado EventSource event source',
    author='Guilherme Souza',
    author_email='guivideojob@gmail.com',
    url='https://github.com/guilhermef/tornado-eventsource',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'tornado>=6.1,<7.0'
    ],

    extras_require={
        'tests': tests_require,
    },

)
