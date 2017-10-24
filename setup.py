#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import sys
import shutil
import setuptools

from sandpaper import const


CURDIR = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(setuptools.Command):

    description = 'Build and publish package'
    user_options = []

    @staticmethod
    def status(status):
        print(('... {status}').format(**locals()))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('removing previous builds')
            shutil.rmtree(os.path.join(CURDIR, 'dist'))
        except FileNotFoundError:
            pass

        self.status('building distribution')
        os.system(('{sys.executable} setup.py sdist').format(**locals()))

        self.status('uploading distribution')
        os.system('twine upload dist/*')

        self.status('pushing git tags')
        os.system(('git tag v{const.module_version}').format(**locals()))
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=const.module_name,
    version=const.module_version,
    description=const.module_description,
    long_description=open(os.path.join(CURDIR, 'README.rst'), 'r').read(),
    license=const.module_license,
    author=const.module_author,
    author_email=const.module_contact,
    url='https://github.com/stephen-bunn/sandpaper',
    platforms='posix',
    include_package_data=True,
    install_requires=list(
        requirement.strip()
        for requirement in open(
            os.path.join(CURDIR, 'requirements.txt'),
            'r'
        ).readlines()
    ),
    packages=setuptools.find_packages(exclude=['tests', 'tests.rules']),
    keywords=[
        'normalization',
        'csv',
        'excel',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Natural Language :: English',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Quality Assurance',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
