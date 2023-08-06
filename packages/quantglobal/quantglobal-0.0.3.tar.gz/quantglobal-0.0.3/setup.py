# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 09:55:40 2022

@author: Local User
"""

from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.3'
DESCRIPTION = 'This package allows access to data provided by Quantitative Global.'

# Setting up
setup(
    name="quantglobal",
    version=VERSION,
    author="Quantitative Global Indices, LLC (Earl Charles)",
    author_email="<echarles@qg-indices.com>",
    description=DESCRIPTION,
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas', 'requests'],
    keywords=['python', 'quantitative finance', 'alternative data', 'statistics', 'stocks'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ]
)

