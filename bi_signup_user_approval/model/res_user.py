# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import logging

from odoo.exceptions import AccessDenied

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    approved_user = fields.Boolean("Approved User")
    first_approval_status = fields.Boolean("First Approval status")
    block_user = fields.Boolean("Block User")

    @api.model
    def create(self, values):
        res = super(ResUsers, self).create(values)
        if res.has_group("base.group_user"):
            _logger.info("Auto Approving Internal User")
            res.approved_user = True
            res.first_approval_status = True
        return res

    # Validate the user
    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        uid = super(ResUsers, cls).authenticate(db, login, password, user_agent_env)
        if uid:
            with cls.pool.cursor() as cr:
                env = api.Environment(cr, uid, {})
                user = env.user
                if not user.approved_user and user._get_signup_invitation_scope() == 'b2c' and not user._is_superuser() and not user._is_admin():
                    raise AccessDenied("Not Approved User")
        return uid

    # Approve user
    def action_approve_user(self):
        for user in self:
            user.approved_user = True
            user.first_approval_status = True
            user.block_user = False
            template = self.env.ref('bi_signup_user_approval.mail_template_user_account_approval',
                                    raise_if_not_found=False)
            if template:
                template.sudo().send_mail(user.id, force_send=True)

    # Reject the user
    def action_reject_user(self):
        for user in self:
            user.approved_user = False
            user.block_user = True
            template = self.env.ref('bi_signup_user_approval.mail_template_user_account_reject',
                                    raise_if_not_found=False)
            if template:
                template.sudo().send_mail(user.id, force_send=True)

    # Block the user
    def action_block_user(self):
        for user in self:
            user.approved_user = False
            user.block_user = True
            user.first_approval_status = False
