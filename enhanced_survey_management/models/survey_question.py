# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Mohammed Savad, Ahammed Harshad  (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0(OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SurveyQuestion(models.Model):
    """ Inherited survey.question to add custom question type"""
    _inherit = 'survey.question'

    selection_ids = fields.One2many('question.selection',
                                    'question_id',
                                    string='Select',
                                    help="""Field used to create selection type
                                     questions""")
    question_type = fields.Selection(selection_add=[
        ('time', 'Time'),
        ('month', 'Month'),
        ('name', 'Name'),
        ('address', 'Address'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('qr', 'Qrcode'),
        ('url', 'URL'),
        ('week', 'Week'),
        ('color', 'Color'),
        ('range', 'Range'),
        ('many2one', 'Many2one'),
        ('date', 'Date'),
        ('many2many', 'Many2many'),
        ('selection', 'Selection'),
        ('barcode', 'Barcode'),
        ('file', 'Upload File')
    ], help="Survey supported question types")
    upload_multiple_file = fields.Boolean(string='Upload Multiple File',
                                          help='Check this box if you want to '
                                               'allow users to upload '
                                               'multiple files')
    matrix_subtype = fields.Selection(
        selection_add=[('custom', 'Custom Matrix')],
        help="""Matrix selection type question""")
    model_id = fields.Many2one('ir.model', string='Model',
                               domain=[('transient', '=', False)],
                               help="Many2one type question")
    range_min = fields.Integer(string='Min',
                               help='Minimum range,range type question')
    range_max = fields.Integer(string='Max',
                               help='Maximum range,range type question')
    qrcode = fields.Text(string='Qrcode',
                         help='Show qrcode in survey')
    qrcode_png = fields.Binary(string='Qrcode PNG', help="Qrcode PNG")
    barcode = fields.Char(string='Barcode', help="Barcode number")
    barcode_png = fields.Binary(string='Barcode PNG',
                                help="Saves barcode png file")
    attachment_type = fields.Selection([
        ('document', 'Document (PDF)'),
        ('image', 'Image (JPG/JPEG)'),
    ], string='Attachment Type', default='document', required=True)
    answer_validation = fields.Selection(
        selection=[
            ('save_as_email', 'Save as user email'),
            ('save_as_nickname', 'Save as user nickname'),
            ('save_as_dob', 'Save as user Date of Birth'),
            ('save_as_postal_address', 'Save as user Postal Address'),
            ('save_as_city', 'Save as user City'),
            ('save_as_country', 'Save as user Country'),
            ('save_as_occupation', 'Save as user Occupation'),
            ('save_as_mobile', 'Save as user Mobile'),
            ('save_as_national_id', 'Save as user National ID/Passport'),
        ],
        string='Answer For',
    )
    max_file_size = fields.Integer("Maximum upload file size (MB)", default=5)
    allow_multi_file = fields.Boolean("Allow upload multiple file", default=False)

    @api.onchange('answer_validation')
    def _check_answer_validation(self):
        for rec in self:
            if rec.answer_validation == 'save_as_email':
                rec.validation_email = True
                rec.save_as_email = True
                rec.save_as_nickname = False
            elif rec.answer_validation == 'save_as_nickname':
                rec.save_as_nickname = True
                rec.validation_email = False
                rec.save_as_email = False
            else:
                rec.validation_email = False
                rec.save_as_email = False
                rec.save_as_nickname = False
    attachment_type = fields.Selection([
        ('document', 'Document (PDF)'),
        ('image', 'Image (JPG/JPEG)'),
    ], string='Attachment Type', default='document',required=True)


    @api.onchange('barcode')
    def _onchange_barcode(self):
        """Onchange function to restrict barcode less-than 12 character """
        if self.barcode:
            if len(self.barcode) < 12:
                raise ValidationError(
                    _("Make sure barcode is at least 12 letters"))
            if len(self.barcode) > 12:
                raise ValidationError(
                    _("There should not be more than 12 "
                      "characters in a barcode"))
            if not self.barcode.isdigit():
                raise ValidationError(_("Only digits are allowed."))

    def get_selection_values(self):
        """Function return options for selection type question"""
        return self.selection_ids

    def prepare_model_id(self, model):
        """Function to return options for many2one question"""
        if model:
            model_data = self.env[model.model].sudo().search([])
            return [rec.read([model_data._rec_name])[0] for rec in model_data]
        model_data = self.env[self.model_id.model].sudo().search([])
        return [rec.read([model_data._rec_name])[0] for rec in model_data]
