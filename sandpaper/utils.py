#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import glob

from path import Path
from braceexpand import braceexpand


def fancy_glob(from_glob, fancy_path=False):
    """ Yields results from fancy globbing with the help of brace expansion.

    For example, the glob pattern ``*.{csv,xls{,x}}`` will result in any
    files using the extensions ``csv``, ``xls``, or ``xlsx`` being yielded.

    :param str from_glob: A fancy glob expresion with optional brace expansion
    :returns: A generator which yields matching file paths
    """

    discovered = set()
    for glob_pattern in list(braceexpand(from_glob)):
        for file_path in glob.glob(glob_pattern):
            if file_path not in discovered:
                discovered.add(file_path)
                yield (Path(file_path) if fancy_path else file_path)
