#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import sys
import shutil
import setuptools


CURDIR = os.path.abspath(os.path.dirname(__file__))
REQUIRES = [
    'six',
    'regex',
    'pyexcel',
    'pyexcel-io',
    'pyexcel-xls',
    'pyexcel-xlsx',
]
RELEASE = {}

# NOTE: important dumb setup for complete segregation of module info
with open(os.path.join(CURDIR, 'sandpaper', '__version__.py'), 'r') as fp:
    exec(fp.read(), RELEASE)


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
        os.system(('{exe} setup.py sdist').format(exe=sys.executable))

        self.status('uploading distribution')
        os.system('twine upload dist/*')

        self.status('pushing git tags')
        os.system(('git tag v{ver}').format(ver=RELEASE['__version__']))
        os.system('git push --tags')

        sys.exit()


setuptools.setup(
    name=RELEASE['__name__'],
    version=RELEASE['__version__'],
    description=RELEASE['__description__'],
    long_description=open(os.path.join(CURDIR, 'README.rst'), 'r').read(),
    license=RELEASE['__license__'],
    author=RELEASE['__author__'],
    author_email=RELEASE['__contact__'],
    url='https://github.com/stephen-bunn/sandpaper',
    include_package_data=True,
    install_requires=REQUIRES,
    packages=setuptools.find_packages(),
    keywords=[
        'normalize',
        'csv',
        'excel',
        'table',
        'clean',
    ],
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
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
