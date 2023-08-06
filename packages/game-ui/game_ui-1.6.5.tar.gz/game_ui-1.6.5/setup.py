#!/usr/bin/python

from setuptools import setup, Extension

Version = '1.6.5'

long_desk = """
Update 1.6.5:
    Updated button;

Documentation - https://github.com/AlmazCode/game_ui#game_ui
"""

setup(
    name='game_ui',
    version=Version,

    author='AlmazCode',
    author_email='diamondplay43@gmail.com',

    description='UI for pygame',
    long_description=long_desk,

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['game_ui'],

    classifiers=['License :: OSI Approved :: Apache Software License',
                'Operating System :: OS Independent',
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: Developers',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',
                'Programming Language :: Python :: Implementation :: PyPy',
                'Programming Language :: Python :: Implementation :: CPython'
                ]
)