from odoo import models, fields, api, _


class Bhseniority(models.Model):
    _inherit = 'hr.employee'

    seniority = fields.Char(string='Seniority', compute='_compute_seniority', compute_sudo=True)

    @api.depends('version_ids.date_start', 'version_ids.date_end')
    def _compute_seniority(self):
        # self.joined_date = self.employee_id.joining_date if self.employee_id.joining_date else ''
        for rec in self:
            today = fields.Date.today()
            first_contract_date = rec.sudo()._get_first_version_date()
            if first_contract_date:
                days = (today - first_contract_date).days
                if days < 365:
                    month = int(days) // 30
                    rec.seniority = _('%s months', month)
                else:
                    year = int(days) // 365
                    month = (int(days) - year * 365) // 30
                    rec.seniority = _('%s years %s months', year, month)
            else:
                rec.seniority = 'Not define'
