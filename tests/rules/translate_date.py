#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import types

from ._common import BaseRuleTest
import sandpaper


class TranslateDateRuleTest(BaseRuleTest):
    """ Tests the ``translate_date`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'translate_date'

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'

    def _application_filter(self, record, column, **kwargs):
        """ Custom date application filter.
        """

        return record['id'] in (2,)

    def test_application(self):
        """ Overridden rule applciation test.
        """

        # NOTE: the applied filters are required for valid test cases
        getattr(self.paper, self.rule_name)(
            from_formats=['%Y-%m-%d', '%Y-%m'],
            to_format="year: %Y | month: %m",
            column_filter=r'name|value',
            callable_filter=self._application_filter
        )
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
