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
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'tornado'
    ],

    extras_require={
        'tests': tests_require,
    },

)
