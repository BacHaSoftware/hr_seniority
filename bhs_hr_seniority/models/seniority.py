import datetime
from datetime import datetime, timedelta
from _datetime import date, datetime
from odoo import models, fields, api, _


class Bhseniority(models.Model):
    _inherit = 'hr.employee'

    seniority = fields.Char(string='Seniority', compute='_compute_seniority')
    joining_first_date = fields.Date(
        string='First Date',
        compute='_compute_joining_first_date',
        store=True,
    )

    def _compute_seniority(self):
        for rec in self:
            today = date.today()
            if rec.joining_first_date:
                days = (today - rec.joining_first_date).days
                if days < 365:
                    month = int(days) // 30
                    rec.seniority = _('%s months', month)
                else:
                    year = int(days) // 365
                    month = (int(days) - year * 365) // 30
                    rec.seniority = _('%s years %s months', year, month)
            else:
                rec.seniority = 'Not define'

    @api.depends('version_ids.contract_date_start')
    def _compute_joining_first_date(self):
        for employee in self:
            versions = employee.sudo().version_ids.filtered(
                lambda v: v.contract_date_start
            ).sorted(key=lambda v: v.contract_date_start)

            employee.joining_first_date = (
                versions[0].contract_date_start if versions else False
            )