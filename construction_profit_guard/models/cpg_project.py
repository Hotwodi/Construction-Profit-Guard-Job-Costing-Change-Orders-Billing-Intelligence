from odoo import api, fields, models


class CpgProject(models.Model):
    _name = 'cpg.project'
    _description = 'Construction Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Project Name', required=True, tracking=True)
    code = fields.Char(string='Project Code', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    project_manager = fields.Many2one('res.users', string='Project Manager', tracking=True, default=lambda self: self.env.user)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    contract_value = fields.Monetary(string='Contract Value', currency_field='currency_id', tracking=True)
    budget_amount = fields.Monetary(string='Budget Amount', currency_field='currency_id', tracking=True)
    committed_cost = fields.Monetary(string='Committed Cost', currency_field='currency_id', compute='_compute_committed_cost', store=True, readonly=False)
    incurred_cost = fields.Monetary(string='Incurred Cost', currency_field='currency_id', compute='_compute_incurred_cost', store=True, readonly=False)
    billed_amount = fields.Monetary(string='Billed Amount', currency_field='currency_id', compute='_compute_billed_amount', store=True, readonly=False)
    completion_pct = fields.Float(string='Completion %', tracking=True, help='Percentage of project completed')
    ai_margin_forecast = fields.Float(string='AI Margin Forecast %', tracking=True, help='AI-predicted profit margin percentage')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], string='Status', default='planned', tracking=True, required=True)

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    cost_code_ids = fields.One2many('cpg.cost.code', 'project_id', string='Cost Codes')
    job_cost_entry_ids = fields.One2many('cpg.job.cost.entry', 'project_id', string='Job Cost Entries')
    change_order_ids = fields.One2many('cpg.change.order', 'project_id', string='Change Orders')
    daily_site_log_ids = fields.One2many('cpg.daily.site.log', 'project_id', string='Daily Site Logs')
    progress_billing_ids = fields.One2many('cpg.progress.billing', 'project_id', string='Progress Billings')
    subcontractor_compliance_ids = fields.One2many('cpg.subcontractor.compliance', 'project_id', string='Subcontractor Compliance')
    commitment_ids = fields.One2many('cpg.commitment', 'project_id', string='Commitments')

    actual_margin = fields.Monetary(string='Actual Margin', currency_field='currency_id', compute='_compute_actual_margin', store=True)
    actual_margin_pct = fields.Float(string='Actual Margin %', compute='_compute_actual_margin', store=True)

    @api.depends('committed_cost', 'incurred_cost')
    def _compute_actual_margin(self):
        for rec in self:
            total_cost = rec.committed_cost or 0.0
            rec.actual_margin = (rec.contract_value or 0.0) - total_cost
            if rec.contract_value:
                rec.actual_margin_pct = (rec.actual_margin / rec.contract_value) * 100.0
            else:
                rec.actual_margin_pct = 0.0

    @api.depends('commitment_ids', 'commitment_ids.committed_amount', 'commitment_ids.state')
    def _compute_committed_cost(self):
        for rec in self:
            rec.committed_cost = sum(rec.commitment_ids.mapped('committed_amount'))

    @api.depends('job_cost_entry_ids', 'job_cost_entry_ids.amount')
    def _compute_incurred_cost(self):
        for rec in self:
            rec.incurred_cost = sum(rec.job_cost_entry_ids.mapped('amount'))

    @api.depends('progress_billing_ids', 'progress_billing_ids.total_billed')
    def _compute_billed_amount(self):
        for rec in self:
            rec.billed_amount = sum(rec.progress_billing_ids.mapped('total_billed'))

    def action_set_active(self):
        self.write({'state': 'active'})

    def action_set_on_hold(self):
        self.write({'state': 'on_hold'})

    def action_set_completed(self):
        self.write({'state': 'completed'})

    def action_set_closed(self):
        self.write({'state': 'closed'})

    def action_ai_forecast(self):
        """Placeholder for AI margin forecast computation."""
        for rec in self:
            if rec.contract_value and rec.incurred_cost:
                projected_cost = rec.incurred_cost / (rec.completion_pct / 100.0) if rec.completion_pct > 0 else rec.incurred_cost
                projected_margin = ((rec.contract_value - projected_cost) / rec.contract_value) * 100.0
                rec.ai_margin_forecast = round(projected_margin, 2)
            else:
                rec.ai_margin_forecast = 0.0
