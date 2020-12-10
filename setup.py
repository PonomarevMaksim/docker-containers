#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name='docker_containers',
    version='0.0.6',
    url='https://github.com/PonomarevMaksim/docker-containers',
    python_requires=">=3.7",
    install_requires=[
        'crayons    >=0.3.0, <1',
        'blindspin  >=2.0.1, <3',
        'docker     >=4.2.0, <5',
    ],
    license="BSD",
    description="Util for start containers",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=get_packages('docker_containers'),
    include_package_data=True,
    data_files=[("", [])],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
