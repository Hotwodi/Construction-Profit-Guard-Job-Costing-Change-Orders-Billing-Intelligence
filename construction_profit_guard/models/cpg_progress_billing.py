from odoo import api, fields, models


class CpgProgressBilling(models.Model):
    _name = 'cpg.progress.billing'
    _description = 'Progress Billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period desc, id desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    billing_number = fields.Char(string='Billing Number', required=True, tracking=True)
    period = fields.Char(string='Period', tracking=True, help='Billing period, e.g. "2025-01" or "Pay App #3"')
    schedule_of_values = fields.Text(string='Schedule of Values', help='Detailed breakdown of work completed by line item')
    previous_billed = fields.Monetary(string='Previous Billed', currency_field='currency_id', tracking=True)
    current_billed = fields.Monetary(string='Current Billed', currency_field='currency_id', tracking=True)
    total_billed = fields.Monetary(string='Total Billed', currency_field='currency_id', compute='_compute_totals', store=True, readonly=False)
    retention_pct = fields.Float(string='Retention %', default=10.0, tracking=True)
    retention_amount = fields.Monetary(string='Retention Amount', currency_field='currency_id', compute='_compute_totals', store=True, readonly=False)
    net_due = fields.Monetary(string='Net Due', currency_field='currency_id', compute='_compute_totals', store=True, readonly=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('invoiced', 'Invoiced'),
    ], string='Status', default='draft', tracking=True, required=True)
    milestone = fields.Char(string='Milestone', tracking=True)

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    @api.depends('previous_billed', 'current_billed', 'retention_pct')
    def _compute_totals(self):
        for rec in self:
            rec.total_billed = (rec.previous_billed or 0.0) + (rec.current_billed or 0.0)
            rec.retention_amount = rec.total_billed * (rec.retention_pct or 0.0) / 100.0
            rec.net_due = rec.total_billed - rec.retention_amount

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_invoice(self):
        self.write({'state': 'invoiced'})

    def action_draft(self):
        self.write({'state': 'draft'})
