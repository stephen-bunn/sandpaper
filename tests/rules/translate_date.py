#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

from ._common import BaseRuleTest


class TranslateDateRuleTest(BaseRuleTest):
    """ Tests the ``translate_date`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'translate_date'

    @property
    def rule_arguments(self):
        """ The arguments for this rule's application.
        """

        return ([{
            '%Y-%m-%d': 'year: %Y | month: %m',
            '%Y-%m': 'year: %Y | month: %m'
        }], {
            'column_filter': r'name|value',
            'value_filter': r'(?:2017|1994).*',
            'callable_filter': self._application_filter
        },)

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'

    def _application_filter(self, record, column, **kwargs):
        """ Custom date application filter.
        """

        return record['id'] in (2,)
