from odoo import api, fields, models


class CpgSubcontractorCompliance(models.Model):
    _name = 'cpg.subcontractor.compliance'
    _description = 'Subcontractor Compliance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'expiry_date, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Subcontractor', tracking=True)
    co_expiry = fields.Date(string='CO Expiry', tracking=True, help='Certificate of Insurance expiry date')
    insurance_type = fields.Char(string='Insurance Type', tracking=True)
    policy_number = fields.Char(string='Policy Number', tracking=True)
    coverage_amount = fields.Monetary(string='Coverage Amount', currency_field='currency_id', tracking=True)
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    compliance_score = fields.Float(string='Compliance Score', tracking=True, help='0-100 compliance score')
    state = fields.Selection([
        ('compliant', 'Compliant'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Status', default='compliant', tracking=True, required=True)

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    @api.onchange('expiry_date')
    def _onchange_expiry_date(self):
        if self.expiry_date:
            today = fields.Date.context_today(self)
            if self.expiry_date < today:
                self.state = 'expired'
            elif (self.expiry_date - today).days <= 30:
                self.state = 'expiring'
            else:
                self.state = 'compliant'

    def action_check_compliance(self):
        """Recompute compliance status based on expiry dates."""
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.expiry_date:
                if rec.expiry_date < today:
                    rec.state = 'expired'
                    rec.compliance_score = 0.0
                elif (rec.expiry_date - today).days <= 30:
                    rec.state = 'expiring'
                    rec.compliance_score = 50.0
                else:
                    rec.state = 'compliant'
                    rec.compliance_score = 100.0
