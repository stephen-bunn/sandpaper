#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import types
import unittest

from sandpaper.utils import (
    fancy_glob,
)

import six
import path


class UtilTest(unittest.TestCase):

    @property
    def static_dir(self):
        """ The path to the utils static testing files.
        """

        if not hasattr(self, '_static_dir'):
            self._static_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                'static/utils/'
            ))
        return self._static_dir

    def assertCountEqual(self, *args, **kwargs):
        if six.PY2:
            self.assertItemsEqual(*args, **kwargs)
        elif six.PY3:
            super().assertCountEqual(*args, **kwargs)

    def test_fancy_glob(self):
        """ Test the ``fancy_glob`` method.
        """

        # test normal glob
        normal_glob = fancy_glob(
            os.path.join(self.static_dir, 'fancy_glob.*.tsv')
        )
        self.assertIsInstance(normal_glob, types.GeneratorType)
        normal_glob = list(normal_glob)
        self.assertIsInstance(normal_glob, list)
        self.assertCountEqual([
            os.path.basename(filepath)
            for filepath in normal_glob
        ], [
            'fancy_glob.1.tsv',
            'fancy_glob.3.tsv',
            'fancy_glob.5.tsv'
        ])

        # test glob with multi value brace expansion
        multi_glob = fancy_glob(
            os.path.join(self.static_dir, 'fancy_glob.1.{c,t}sv')
        )
        self.assertIsInstance(multi_glob, types.GeneratorType)
        multi_glob = list(multi_glob)
        self.assertIsInstance(multi_glob, list)
        self.assertCountEqual([
            os.path.basename(filepath)
            for filepath in multi_glob
        ], [
            'fancy_glob.1.csv',
            'fancy_glob.1.tsv'
        ])

        # test a glob with brace expansion ranges
        range_glob = fancy_glob(
            os.path.join(self.static_dir, 'fancy_glob.{1..5}.csv')
        )
        self.assertIsInstance(range_glob, types.GeneratorType)
        range_glob = list(range_glob)
        self.assertIsInstance(range_glob, list)
        self.assertCountEqual([
            os.path.basename(filepath)
            for filepath in range_glob
        ], [
            'fancy_glob.1.csv',
            'fancy_glob.2.csv',
            'fancy_glob.5.csv'
        ])

        # test fancy 3rd party path object usage
        path_glob = fancy_glob(
            os.path.join(self.static_dir, 'fancy_glob.{1,5}.{t,c}sv'),
            fancy_path=True
        )
        self.assertIsInstance(path_glob, types.GeneratorType)
        path_glob = list(path_glob)
        self.assertIsInstance(path_glob, list)
        for path_obj in path_glob:
            self.assertIsInstance(path_obj, path.Path)
        self.assertCountEqual([
            path_obj.basename()
            for path_obj in path_glob
        ], [
            'fancy_glob.1.tsv',
            'fancy_glob.1.csv',
            'fancy_glob.5.tsv',
            'fancy_glob.5.csv'
        ])
