# -*- coding: utf-8 -*-
#############################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, api


class HrPayslip(models.Model):
    """ Extends the 'hr.payslip' model to include
    additional functionality related to employee loans."""
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        """Compute additional inputs for the employee payslip,
        considering active loans.
        :param contract_ids: Contract ID of the current employee.
        :param date_from: Start date of the payslip.
        :param date_to: End date of the payslip.
        :return: List of dictionaries representing additional inputs for
        the payslip."""
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from,
                                                date_to)
        employee_id = self.env['hr.contract'].browse(
            contract_ids[0].id).employee_id if contract_ids \
            else self.employee_id
        loan_id = self.env['hr.loan'].search(
            [('employee_id', '=', employee_id.id), ('state', '=', 'approve')])
        for loan in loan_id:
            for loan_line in loan.loan_lines:
                if (date_from <= loan_line.date <= date_to and
                        not loan_line.paid):
                    for result in res:
                        if result.get('code') == 'LO':
                            result['amount'] = loan_line.amount
                            result['loan_line_id'] = loan_line.id
        return res

    def action_payslip_done(self):
        """ Compute the loan amount and remaining amount while confirming
            the payslip"""
        for line in self.input_line_ids:
            if line.loan_line_id:
                line.loan_line_id.paid = True
                line.loan_line_id.loan_id._compute_total_amount()
        return super(HrPayslip, self).action_payslip_done()

    @api.onchange('employee_id', 'date_from', 'date_to')
    def _onchange_employee_other_inputs(self):
        """Function for getting contract for employee"""
        input_lines = []
        self.input_line_ids = False
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        loan_id = self.env['hr.loan'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'approve')])
        for loan in loan_id:
            for loan_line in loan.loan_lines:
                if (self.date_from <= loan_line.date <= self.date_to and not loan_line.paid):
                    input_type_id = self.env["hr.payslip.input.type"].search([("code", "=", "LOAN_DEDUCTION")], limit=1)
                    input_lines.append((0, 0, {
                        "input_type_id": input_type_id and input_type_id.id or False,
                        "loan_line_id": loan_line.id,
                        "name": loan_line.loan_id.name + loan_line.loan_id.loan_type.name if loan_line.loan_id.loan_type else '',
                        "amount": loan_line.amount
                        }))
        self.input_line_ids = input_lines
        return
