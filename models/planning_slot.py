from odoo import models, fields

class PlanningSlot(models.Model):
    _inherit = 'planning.slot'

    task_id = fields.Many2one('project.task', string='Linked Task', readonly=True)
