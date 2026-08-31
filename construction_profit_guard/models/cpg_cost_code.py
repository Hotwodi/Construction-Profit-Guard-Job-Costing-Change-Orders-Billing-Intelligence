from odoo import api, fields, models


class CpgCostCode(models.Model):
    _name = 'cpg.cost.code'
    _description = 'Cost Code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    cost_type = fields.Selection([
        ('labor', 'Labor'),
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('subcontractor', 'Subcontractor'),
        ('overhead', 'Overhead'),
    ], string='Cost Type', required=True, default='material', tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    budget_amount = fields.Monetary(string='Budget Amount', currency_field='currency_id', tracking=True)
    committed_cost = fields.Monetary(string='Committed Cost', currency_field='currency_id', compute='_compute_costs', store=True, readonly=False)
    actual_cost = fields.Monetary(string='Actual Cost', currency_field='currency_id', compute='_compute_costs', store=True, readonly=False)
    variance = fields.Monetary(string='Variance', currency_field='currency_id', compute='_compute_variance', store=True)
    ai_overrun_risk = fields.Float(string='AI Overrun Risk %', tracking=True, help='AI-predicted probability of budget overrun')

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    job_cost_entry_ids = fields.One2many('cpg.job.cost.entry', 'cost_code_id', string='Job Cost Entries')
    commitment_ids = fields.One2many('cpg.commitment', 'cost_code_id', string='Commitments')

    @api.depends('job_cost_entry_ids', 'job_cost_entry_ids.amount', 'commitment_ids', 'commitment_ids.committed_amount')
    def _compute_costs(self):
        for rec in self:
            rec.actual_cost = sum(rec.job_cost_entry_ids.mapped('amount'))
            rec.committed_cost = sum(rec.commitment_ids.mapped('committed_amount'))

    @api.depends('budget_amount', 'actual_cost')
    def _compute_variance(self):
        for rec in self:
            rec.variance = (rec.budget_amount or 0.0) - (rec.actual_cost or 0.0)

    def action_ai_overrun_check(self):
        """Placeholder for AI overrun risk computation."""
        for rec in self:
            if rec.budget_amount and rec.actual_cost:
                utilization = rec.actual_cost / rec.budget_amount
                risk = min(100.0, utilization * 100.0)
                rec.ai_overrun_risk = round(risk, 2)
            else:
                rec.ai_overrun_risk = 0.0
