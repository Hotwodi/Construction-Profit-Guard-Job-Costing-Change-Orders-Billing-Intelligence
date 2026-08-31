from odoo import api, fields, models


class CpgDailySiteLog(models.Model):
    _name = 'cpg.daily.site.log'
    _description = 'Daily Site Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'log_date desc, id desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    project_id = fields.Many2one('cpg.project', string='Project', required=True, ondelete='cascade', tracking=True)
    log_date = fields.Date(string='Log Date', required=True, default=fields.Date.context_today, tracking=True)
    weather = fields.Char(string='Weather', tracking=True)
    temperature = fields.Float(string='Temperature (°F)', tracking=True)
    labor_count = fields.Integer(string='Labor Count', tracking=True)
    equipment_used = fields.Text(string='Equipment Used')
    deliveries = fields.Text(string='Deliveries')
    blockers = fields.Text(string='Blockers')
    safety_notes = fields.Text(string='Safety Notes')
    photos = fields.Many2many('ir.attachment', string='Photos')
    submitted_by = fields.Many2one('res.users', string='Submitted By', default=lambda self: self.env.user, tracking=True)
    ai_change_order_flags = fields.Text(string='AI Change Order Flags', help='AI-detected items that may require change orders')

    company_id = fields.Many2one('res.company', string='Company', related='project_id.company_id', store=True)

    def action_ai_detect_change_orders(self):
        """Placeholder for AI change order detection from daily log."""
        for rec in self:
            flags = []
            if rec.blockers and rec.blockers.strip():
                flags.append('Blockers detected: %s' % rec.blockers)
            if rec.deliveries and rec.deliveries.strip():
                flags.append('Deliveries logged: %s' % rec.deliveries)
            rec.ai_change_order_flags = '\n'.join(flags) if flags else ''
