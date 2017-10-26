#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import types

from ._common import BaseRuleTest
import sandpaper


class TranslateTextRuleTest(BaseRuleTest):
    """ Tests the ``translate_text`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'translate_text'

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'

    def test_application(self):
        """ Overridden rule applciation test.
        """

        getattr(self.paper, self.rule_name)(
            from_regex=r'He(L+)o',
            to_format="L's: {0}"
        )
        applied = self.paper.apply(self._get_static_glob(post=False))
        self.assertIsInstance(applied, types.GeneratorType)
        applied = list(applied)
        self.assertIsInstance(applied, list)

        for (evaluation, processed) in zip(
            sandpaper.utils.fancy_glob(self._get_static_glob(post=True)),
            applied
        ):
            print((evaluation, processed[0],))
            self.assertEqual(
                self._get_file_hash(evaluation),
                self._get_file_hash(processed[0])
            )
            self.assertIsInstance(processed[-1], dict)
