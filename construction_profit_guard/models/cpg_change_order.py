from odoo import api, fields, models


class CpgChangeOrder(models.Model):
    _name = 'cpg.change.order'
    _description = 'Change Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'approved_date desc, id desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    co_number = fields.Char(string='CO Number', required=True, tracking=True)
    description = fields.Text(string='Description')
    estimated_cost = fields.Monetary(string='Estimated Cost', currency_field='currency_id', tracking=True)
    approved_cost = fields.Monetary(string='Approved Cost', currency_field='currency_id', tracking=True)
    status = fields.Selection([
        ('requested', 'Requested'),
        ('estimated', 'Estimated'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('invoiced', 'Invoiced'),
    ], string='Status', default='requested', tracking=True, required=True)
    customer_approved = fields.Boolean(string='Customer Approved', default=False, tracking=True)
    approved_date = fields.Date(string='Approved Date', tracking=True)
    ai_detected_from = fields.Text(string='AI Detected From', help='Source from which AI detected this change order (e.g., daily log, vendor bill)')

    currency_id = fields.Many2one('res.currency', string='Currency', related='project_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    def action_approve(self):
        self.write({'status': 'approved', 'customer_approved': True, 'approved_date': fields.Date.context_today(self), 'approved_cost': self.estimated_cost})

    def action_reject(self):
        self.write({'status': 'rejected'})

    def action_invoice(self):
        self.write({'status': 'invoiced'})

    def action_set_estimated(self):
        self.write({'status': 'estimated'})
