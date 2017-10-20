#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import setuptools

from sandpaper import const


setuptools.setup(
    name=const.module_name,
    version=const.module_version,
    description=const.module_description,
    long_description=open('README.rst', 'r').read(),
    license=const.module_license,
    author=const.module_author,
    author_email=const.module_contact,
    url='https://github.com/stephen-bunn/sandpaper',
    platforms='Unix',
    include_package_data=True,
    install_requires=[
        requirement.split('--hash')[0].strip()
        for requirement in open('requirements.txt', 'r').readlines()
    ],
    packages=[
        'sandpaper'
    ]
)
