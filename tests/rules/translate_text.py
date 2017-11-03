#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

from ._common import BaseRuleTest


class TranslateTextRuleTest(BaseRuleTest):
    """ Tests the ``translate_text`` rule.
    """

    @property
    def rule_name(self):
        """ The name of the rule.
        """

        return 'translate_text'

    @property
    def rule_arguments(self):
        """ The arguments for this rule's application.
        """

        return (
            [{r'He(L+)o': "L's: {0}"}],
            {},
        )

    @property
    def rule_group(self):
        """ The group type of the rule.
        """

        return 'value_rules'
