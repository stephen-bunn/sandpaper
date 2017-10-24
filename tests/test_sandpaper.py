#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import unittest

import sandpaper

import six


class SandPaperTest(unittest.TestCase):
    """ The base SandPaper class test.
    """

    def setUp(self):
        """ Setup the test.
        """

        self.named_paper = sandpaper.SandPaper('test')
        self.blank_paper = sandpaper.SandPaper()

    def tearDown(self):
        """ Clear the execution of the test.
        """

        del self.named_paper
        del self.blank_paper

    def test_initialization(self):
        """ Test class initialization.
        """

        # test named initialization
        self.assertIsInstance(self.named_paper.name, six.string_types)
        self.assertEqual(self.named_paper.name, 'test')
        self.assertIsInstance(self.named_paper.value_rules, list)
        self.assertEqual(self.named_paper.value_rules, [])
        self.assertIsInstance(self.named_paper.record_rules, list)
        self.assertEqual(self.named_paper.record_rules, [])
        self.assertNotEqual(self.named_paper.name, self.named_paper.uid)
        self.assertIsInstance(self.named_paper.__repr__(), six.string_types)

        # test blank initialization
        self.assertIsInstance(self.blank_paper.name, six.string_types)
        # NOTE: unknown hash for blank paper name with no rules
        # just check that it isn't blank
        self.assertGreater(len(self.blank_paper.name), 0)
        self.assertIsInstance(self.blank_paper.value_rules, list)
        self.assertEqual(self.blank_paper.value_rules, [])
        self.assertIsInstance(self.blank_paper.record_rules, list)
        self.assertEqual(self.blank_paper.record_rules, [])
        self.assertEqual(self.blank_paper.name, self.blank_paper.uid)
        self.assertIsInstance(self.blank_paper.__repr__(), six.string_types)

    def test_equality(self):
        """ Test instance equality.
        """

        # instances without rules are equal (regardless of names)
        self.assertEqual(self.named_paper, self.blank_paper)
        self.assertNotEqual(
            self.named_paper.__repr__(),
            self.blank_paper.__repr__()
        )

        # instances with different value rules are not the same
        self.named_paper.lower()
        self.assertNotEqual(self.named_paper, self.blank_paper)

        # same value rules mean instances are the same
        self.blank_paper.lower()
        self.assertEqual(self.named_paper, self.blank_paper)
        self.assertNotEqual(
            self.named_paper.__repr__(),
            self.blank_paper.__repr__()
        )

        # validate value rule removal
        del self.named_paper.value_rules[:]
        del self.blank_paper.value_rules[:]
        self.assertEqual(self.named_paper, self.blank_paper)
        self.assertNotEqual(
            self.named_paper.__repr__(),
            self.blank_paper.__repr__()
        )

        # different record rules mean instances are different
        self.named_paper.add_column(column_name='test', column_value='test')
        self.assertNotEqual(self.named_paper, self.blank_paper)

        # same record rules man instances are equal
        self.blank_paper.add_column(column_name='test', column_value='test')
        self.assertEqual(self.named_paper, self.blank_paper)
        self.assertNotEqual(
            self.named_paper.__repr__(),
            self.blank_paper.__repr__()
        )

        # validate record rule removal
        del self.named_paper.record_rules[:]
        del self.blank_paper.record_rules[:]
        self.assertEqual(self.named_paper, self.blank_paper)
        self.assertNotEqual(
            self.named_paper.__repr__(),
            self.blank_paper.__repr__()
        )

    def test_serialization(self):
        """ Tests instance exporting and loading.
        """

        # assert instances start out the same
        self.assertEqual(self.named_paper, self.blank_paper)

        # ensure serialization between export and load functions
        named_export = self.named_paper.export()
        self.assertIsInstance(named_export, dict)
        named_load = sandpaper.SandPaper.load(named_export)
        self.assertIsInstance(named_load, sandpaper.SandPaper)
        self.assertEqual(named_load, self.named_paper)

        # ensure serialization of equality objects are the same
        blank_export = self.blank_paper.export()
        self.assertIsInstance(blank_export, dict)
        blank_load = sandpaper.SandPaper.load(blank_export)
        self.assertIsInstance(blank_load, sandpaper.SandPaper)
        self.assertEqual(named_load, blank_load)
        self.assertEqual(blank_load, self.blank_paper)

        # ensure serialization of ruled objects are not the same
        self.named_paper.lower()
        named_export_modified = self.named_paper.export()
        self.assertIsInstance(named_export_modified, dict)
        self.assertNotEqual(named_export_modified, named_export)
        named_export_load = sandpaper.SandPaper.load(named_export_modified)
        self.assertIsInstance(named_export_load, sandpaper.SandPaper)
        self.assertEqual(named_export_load, self.named_paper)

        # clean rule changes
        del self.named_paper.value_rules[:]
