#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import abc
import types
import hashlib
import unittest

import sandpaper

import six


class BaseRuleTest(six.with_metaclass(abc.ABCMeta, unittest.TestCase)):
    """ The base rule test.
    """

    @abc.abstractproperty
    def rule_name(self):
        """ Required rule name for static path discovery.
        """

        raise NotImplementedError()

    @abc.abstractproperty
    def rule_group(self):
        """ Required rule group for static path discovery.
        """

        raise NotImplementedError()

    @property
    def static_dir(self):
        """ The path to the rule's static testing files.
        """

        if not hasattr(self, '_static_dir'):
            self._static_dir = os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                ('static/rules/{self.rule_name}').format(self=self)
            ))
        return self._static_dir

    def _get_static_glob(self, post=False):
        """ Gets a glob for testing static files.
        """

        return os.path.join(
            self.static_dir,
            '{flag}.{{xls{{,x}},{{c,t}}sv}}'
        ).format(flag=('post' if post else 'pre'))

    def _get_file_hash(self, filepath, chunk_size=4096):
        """ Hashes a filepath for equality validation.
        """

        hasher = hashlib.md5()
        with open(filepath, 'rb') as fp:
            while True:
                chunk = fp.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    def setUp(self):
        """ Setup the test.
        """

        self.paper = sandpaper.SandPaper()

    def tearDown(self):
        """ Clear the execution of the test.
        """

        del self.paper

    def test_exists(self):
        """ Test that the rule exists.
        """

        self.assertTrue(callable(getattr(self.paper, self.rule_name)))

    def test_addition(self):
        """ Test the addition of the rule.
        """

        self.assertIsInstance(getattr(self.paper, self.rule_group), list)
        self.assertEqual(getattr(self.paper, self.rule_group), [])
        getattr(self.paper, self.rule_name)()
        self.assertIsInstance(getattr(self.paper, self.rule_group), list)
        self.assertGreater(len(getattr(self.paper, self.rule_group)), 0)

        del getattr(self.paper, self.rule_group)[:]

    def test_application(self):
        """ Tests the implementation of the rule.
        """

        getattr(self.paper, self.rule_name)()

        applied = self.paper.apply(self._get_static_glob(post=False))
        self.assertIsInstance(applied, types.GeneratorType)
        applied = list(applied)
        self.assertIsInstance(applied, list)

        for (evaluation, processed) in zip(
            sandpaper.utils.fancy_glob(self._get_static_glob(post=True)),
            applied
        ):
            print((evaluation, processed,))
            self.assertEqual(
                self._get_file_hash(evaluation),
                self._get_file_hash(processed)
            )
