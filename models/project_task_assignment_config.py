from odoo import models, fields

class ProjectTaskAssignmentConfig(models.Model):
    _name = 'project.task.assignment.config'
    _description = 'Task Assignment Configuration'

    # Enable or disable the feature globally
    is_enabled = fields.Boolean(string="Enable Task Assignment Control", default=True)

    # Behavior: warn or block
    behavior = fields.Selection([
        ('warn', 'Warning Only'),
        ('block', 'Block Assignment')
    ], string="Behavior", default='warn')
