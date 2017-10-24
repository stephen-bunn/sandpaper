#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import sys


class _const(object):
    """ SandPaper module constants container.
    """

    __module_name = 'sandpaper'
    __module_version = '0.0.0'
    __module_description = 'Simplified table-type data normalization'
    __module_author = 'Stephen Bunn'
    __module_contact = 'stephen@bunn.io'
    __module_contributors = tuple()
    __module_license = 'MIT License'
    __module_classifiers = (
        'Development Status :: 2 - Pre-Alpha',
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
    )

    @property
    def module_name(self):
        """ The name of the module.

        :getter: Returns the name of the module
        :rtype: str
        """

        return self.__module_name

    @property
    def module_version(self):
        """ The name of the module.

        :getter: Returns the name of the module
        :rtype: str
        """

        return self.__module_version

    @property
    def module_description(self):
        """ The description of the module.

        :getter: Returns the description of the module
        :rtype: str
        """

        return self.__module_description

    @property
    def module_author(self):
        """ The author of the module.

        :getter: Returns the author of the module
        :rtype: str
        """

        return self.__module_author

    @property
    def module_contact(self):
        """ The contact info for the author of the module.

        :getter: Returns the contact info for the author of the module
        :rtype: str
        """

        return self.__module_contact

    @property
    def module_contributors(self):
        """ The contributors to the module.

        :getter: Returns the contributors to the module
        :rtype: tuple(str)
        """

        return self.__module_contributors

    @property
    def module_license(self):
        """ The license of the module.

        :getter: Returns the license of the module
        :rtype: str
        """

        return self.__module_license

    @property
    def module_classifiers(self):
        """ The classifiers of the module.

        :getter: Returns the classifiers of the module
        :setter: tuple(str)
        """

        return self.__module_classifiers


sys.modules[__name__] = _const()
