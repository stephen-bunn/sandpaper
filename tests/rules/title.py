#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

from ._common import BaseRuleTest


class TitleRuleTest(BaseRuleTest):
    """ Tests the ``title`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'title'

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'
