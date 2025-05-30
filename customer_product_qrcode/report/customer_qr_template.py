# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:Anjhana A K(<https://www.cybrosys.com>)
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, api
from odoo.http import request


class CustomerQrTemplate(models.AbstractModel):
    """Abstract model for generating the customer QR template report."""
    _name = 'report.customer_product_qrcode.customer_qr_template'
    _description = 'Customer QR'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get the report values for generating the customer QR template."""
        if 'context' in data:
            ctx = data.get('context')
            if ctx.get('active_model') == 'res.partner':
                data['type'] = 'cust'
                data['data'] = int(ctx.get('active_id'))
        if data['type'] == 'cust':
            dat = [request.env['res.partner'].browse(data['data'])]
        elif data['type'] == 'all':
            dat = [request.env['product.product'].search(
                [('product_tmpl_id', '=', data['data'])])]
        else:
            dat = request.env['product.product'].browse(data['data'])
        return {
            'data': dat,
        }
