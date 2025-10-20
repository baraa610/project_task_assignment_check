from odoo import models, fields, api, _


class UncoveredTaskAlert(models.Model):
    _name = 'uncovered.task.alert'
    _description = 'Uncovered Task Alert'
    _order = 'create_date desc'
    _rec_name = 'task_id'

    task_id = fields.Many2one(
        'project.task',
        string='Task',
        required=True,
        ondelete='cascade',
    )

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        related='task_id.project_id',
        store=True,
    )

    assigned_user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        required=False,
    )

    reason = fields.Text(
        string='Reason',
        required=True,
    )

    availability_status = fields.Selection([
        ('on_leave', 'On Leave'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ], string='Status', required=True)

    state = fields.Selection([
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ], string='State', default='active', required=True)

    resolved_date = fields.Datetime(string='Resolved Date')
    resolved_by_id = fields.Many2one('res.users', string='Resolved By')

    notes = fields.Text(string='Notes')

    def action_resolve(self):
        """Mark alert as resolved"""
        self.write({
            'state': 'resolved',
            'resolved_date': fields.Datetime.now(),
            'resolved_by_id': self.env.user.id,
        })

    def action_dismiss(self):
        """Dismiss the alert"""
        self.write({
            'state': 'dismissed',
            'resolved_date': fields.Datetime.now(),
            'resolved_by_id': self.env.user.id,
        })

    def action_open_task(self):
        """Open related task"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Task'),
            'res_model': 'project.task',
            'res_id': self.task_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
