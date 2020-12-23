#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from tornado_eventsource import __version__

tests_require = [
    'coverage',
    'nose',
    'mock'
]

setup(
    name='tornado_eventsource',
    version=__version__,
    description="EventSource handler for tornado",
    long_description="A simple EventSource handler for tornado",
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
        'tornado>=3.2.0,<4.0'
    ],

    extras_require={
        'tests': tests_require,
    },

)
