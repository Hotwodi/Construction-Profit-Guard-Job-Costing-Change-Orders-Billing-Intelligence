from odoo import api, fields, models


class CpgJobCostEntry(models.Model):
    _name = 'cpg.job.cost.entry'
    _description = 'Job Cost Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    cost_code_id = fields.Many2one('cpg.cost.code', string='Cost Code', required=True, tracking=True)
    entry_type = fields.Selection([
        ('po', 'Purchase Order'),
        ('timesheet', 'Timesheet'),
        ('vendor_bill', 'Vendor Bill'),
        ('inventory', 'Inventory'),
        ('manual', 'Manual'),
    ], string='Entry Type', required=True, default='manual', tracking=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', tracking=True)
    description = fields.Text(string='Description')
    ai_categorized = fields.Boolean(string='AI Categorized', default=False, help='Whether this entry was auto-categorized by AI')

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {'domain': {'cost_code_id': [('project_id', '=', self.project_id.id)]}}

    def action_ai_categorize(self):
        """Placeholder for AI auto-categorization."""
        for rec in self:
            rec.ai_categorized = True
