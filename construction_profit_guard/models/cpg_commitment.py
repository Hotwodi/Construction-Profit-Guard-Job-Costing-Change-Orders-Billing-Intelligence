from odoo import api, fields, models


class CpgCommitment(models.Model):
    _name = 'cpg.commitment'
    _description = 'Commitment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    cost_code_id = fields.Many2one('cpg.cost.code', string='Cost Code', required=True, tracking=True)
    commitment_type = fields.Selection([
        ('po', 'Purchase Order'),
        ('subcontract', 'Subcontract'),
        ('inventory_transfer', 'Inventory Transfer'),
    ], string='Commitment Type', required=True, default='po', tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', tracking=True)
    committed_amount = fields.Monetary(string='Committed Amount', currency_field='currency_id', required=True, tracking=True)
    incurred_to_date = fields.Monetary(string='Incurred To Date', currency_field='currency_id', tracking=True)
    remaining = fields.Monetary(string='Remaining', currency_field='currency_id', compute='_compute_remaining', store=True, readonly=False)
    state = fields.Selection([
        ('open', 'Open'),
        ('partial', 'Partial'),
        ('completed', 'Completed'),
    ], string='Status', default='open', tracking=True, required=True)

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    @api.depends('committed_amount', 'incurred_to_date')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining = (rec.committed_amount or 0.0) - (rec.incurred_to_date or 0.0)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {'domain': {'cost_code_id': [('project_id', '=', self.project_id.id)]}}

    def action_set_partial(self):
        self.write({'state': 'partial'})

    def action_set_completed(self):
        self.write({'state': 'completed'})
