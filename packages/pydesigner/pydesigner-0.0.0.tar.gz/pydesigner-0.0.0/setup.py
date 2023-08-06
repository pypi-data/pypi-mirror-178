#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import pydesigner

with open("README.md", "r", encoding='utf-8') as fs:
    README = fs.read()

setup(
    name="pydesigner",
    version=pydesigner.__version__,
    author="liuzimin",
    author_email="737210395@qq.com",
    description="opened,freed,designer",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/liuzimin/pydesigner",
    packages=find_packages(),
    install_requires=[
        "ply >= 3.11",
        ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
