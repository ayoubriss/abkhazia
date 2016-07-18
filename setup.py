#!/usr/bin/env python
# Copyright 2016 Thomas Schatz, Xuan Nga Cao, Mathieu Bernard
#
# This file is part of abkhazia: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abkhazia is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with abkahzia. If not, see <http://www.gnu.org/licenses/>.
"""Setup script for the abkhazia package"""

import os
from setuptools import setup, find_packages

GITHUB_BOOTPHON = 'https://github.com/bootphon/'
SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = '0.3'

# On Reads The Docs we don't install any package
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'
REQUIREMENTS = [] if ON_RTD else [
    # 'abnet',
    # 'ABXpy',
    # 'cpickle',
    # 'matplotlib',
    # 'pandas',
    # 'yaafelib',
    'numpy',
    'progressbar2',
    'joblib',
    'argcomplete',
    'pytest',
    'h5features>=1.1',
    'phonemizer>=0.2'
]

setup(
    name='abkhazia',
    version=VERSION,
    packages=find_packages(exclude=['test']),
    zip_safe=False,
    scripts=[],

    # install dependancies from bootphon github
    dependency_links=[GITHUB_BOOTPHON + package for package in (
        'phonemizer/archive/v0.2.tar.gz#egg=phonemizer-0.2',
        'h5features/archive/v1.1.tar.gz#egg=h5features-1.1',
        # 'ABXpy/archive/v0.2.tar.gz#egg=ABXpy-0.2'
    )],

    # install python dependencies from PyPI
    install_requires=REQUIREMENTS,

    # include any files in abkhazia/share
    package_data={
        'abkhazia': ['share/*.*', 'share/kaldi_templates/*']
    },

    # define the command-line script to use
    entry_points={
        'console_scripts': ['abkhazia = abkhazia.commands.abkhazia_main:main']},

    # metadata for upload to PyPI
    author='Thomas Schatz, Mathieu Bernard, Roland Thiolliere, Xuan Nga Cao',
    author_email='mmathieubernardd@gmail.com',
    description='ABX and kaldi experiments on speech corpora made easy',
    license='GPL3',
    keywords='speech corpus ASR kaldi ABX',
    url='https://github.com/bootphon/abkhazia',
    long_description=open('README.md').read(),
)
