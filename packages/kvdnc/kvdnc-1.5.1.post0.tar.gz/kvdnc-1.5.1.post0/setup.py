# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="kvdnc",
    version="1.5.1-0",
    description="kvdn client library and tool",
    license="Apache",
    author="Grant Haywood",
    packages=["kvdn_client","kvdn-cli"],
    install_requires=["httplib2"],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
