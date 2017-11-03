#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

from ._common import BaseRuleTest


class AddColumnsRuleTest(BaseRuleTest):
    """ Tests the ``add_columns`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'add_columns'

    @property
    def rule_arguments(self):
        """ The arguments for this rule's application.
        """

        return ([{'test': 'test_value'}], {},)

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'record_rules'
