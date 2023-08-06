# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 19:14:29 2022

@author: Local User
"""

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'This package allows access to data provided by Quantitative Global Indices.'

# Setting up
setup(
    name="quant-global",
    version=VERSION,
    author="Quantitative Global Indices, LLC (Earl Charles)",
    author_email="<echarles@qg-indices.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas', 'requests'],
    keywords=['python', 'quantitative finance', 'alternative data', 'statistics', 'stocks'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ]
)