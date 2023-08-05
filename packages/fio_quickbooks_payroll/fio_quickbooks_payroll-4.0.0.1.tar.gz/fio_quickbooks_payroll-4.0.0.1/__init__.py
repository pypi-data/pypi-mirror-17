# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool

from quickbooks import PayrollAccount, ImportPayrollItemStart, ImportPayrollItem
from employee import Employee


def register():
    Pool.register(
        PayrollAccount,
        Employee,
        ImportPayrollItemStart,
        module='quickbooks_payroll', type_='model'
    )
    Pool.register(
        ImportPayrollItem,
        module='quickbooks_payroll', type_='wizard'
    )
