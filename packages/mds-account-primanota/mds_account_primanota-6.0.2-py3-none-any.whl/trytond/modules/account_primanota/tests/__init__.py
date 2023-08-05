# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.account_primanota.tests.test_primanota import PMTestCase

__all__ = ['suite']

class PrimanotaTestCase(\
    PMTestCase,
    ):
    'Test pm module'
    module = 'account_primanota'

# end PrimanotaTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PrimanotaTestCase))
    return suite
