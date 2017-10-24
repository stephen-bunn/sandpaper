#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import types

from ._common import BaseRuleTest
import sandpaper


class SubstituteRuleTest(BaseRuleTest):
    """ Tests the ``substitute`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'substitute'

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'

    def test_application(self):
        """ Overridden rule applciation test.
        """

        getattr(self.paper, self.rule_name)(substitutes={
            r'^T.*': 'SUBSTITUTED01',
            r'HeL+o': 'SUBSTITUTED02'
        })
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
