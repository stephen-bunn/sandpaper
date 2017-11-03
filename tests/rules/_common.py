#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import os
import abc
import glob
import filecmp
import unittest

import sandpaper

import six
import braceexpand


class BaseRuleTest(six.with_metaclass(abc.ABCMeta, unittest.TestCase)):
    """ The base rule test.
    """

    @abc.abstractproperty
    def rule_name(self):
        """ Required rule name for static path discovery.
        """

        raise NotImplementedError()

    @abc.abstractproperty
    def rule_arguments(self):
        """ Required rule arguments as a tuple (*args, **kwargs).
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

    def _evaluate_glob(self, pattern):
        discovered = set()
        for variation in braceexpand.braceexpand(pattern):
            for path in glob.glob(variation):
                discovered.add(path)
        return discovered

    def _get_static_glob(self, post=False):
        """ Gets a glob for testing static files.
        """

        return os.path.join(
            self.static_dir,
            '{flag}.{{xls{{,x}},{{c,t}}sv}}'
        ).format(flag=('post' if post else 'pre'))

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

        self.assertIsInstance(getattr(self.paper, 'rules'), list)
        self.assertEqual(len(getattr(self.paper, 'rules')), 0)
        self.assertIsInstance(getattr(self.paper, self.rule_group), set)
        self.assertEqual(getattr(self.paper, self.rule_group), set())
        getattr(self.paper, self.rule_name)()
        self.assertGreater(len(getattr(self.paper, 'rules')), 0)
        self.assertIsInstance(getattr(self.paper, self.rule_group), set)
        self.assertGreater(len(getattr(self.paper, self.rule_group)), 0)

        del self.paper.rules[:]

    def test_application(self):
        """ Tests the implementation of the rule.
        """

        getattr(self.paper, self.rule_name)(
            *self.rule_arguments[0],
            **self.rule_arguments[-1]
        )

        (pre_paths, sanded_paths, post_paths,) = (
            self._evaluate_glob(self._get_static_glob(post=False)),
            [],
            self._evaluate_glob(self._get_static_glob(post=True)),
        )
        for path in pre_paths:
            (name, ext,) = os.path.splitext(path)
            sanded_paths.append(('{name}.sanded{ext}').format(**locals()))

        for (from_file, to_file, result_file,) in \
                zip(pre_paths, sanded_paths, post_paths):
            print((from_file, to_file, result_file,))
            applied = self.paper.apply(from_file, to_file)
            print(applied)
            self.assertEqual(applied, to_file)
            self.assertTrue(filecmp.cmp(to_file, result_file))
