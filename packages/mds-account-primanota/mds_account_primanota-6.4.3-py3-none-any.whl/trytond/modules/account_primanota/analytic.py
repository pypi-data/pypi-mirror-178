# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.pool import PoolMeta
from trytond.model import fields


class PrimaNotaAnalytic(metaclass=PoolMeta):
    __name__ = 'account_primanota.primanota'

    analytic_lines = fields.One2Many(string='Analytic Lines',
        model_name='analytic_account.line', field='move_line',
        readonly=True)

# end PrimaNotaAnalytic
