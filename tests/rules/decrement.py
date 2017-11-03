#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

from ._common import BaseRuleTest


class DecrementRuleTest(BaseRuleTest):
    """ Tests the ``decrement`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'decrement'

    @property
    def rule_arguments(self):
        """ The arguments for this rule's application.
        """

        return ([], {'amount': 1},)

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'
