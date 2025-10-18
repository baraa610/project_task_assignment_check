from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Field to store reason if assignment override occurs
    override_reason = fields.Text(string="Reason for Override")

    @api.constrains('user_id', 'date_deadline', 'planned_date_begin')
    def _check_assignee_availability(self):
        """Server-side constraint to prevent assignment if user is on leave or busy"""
        Config = self.env['project.task.assignment.config'].sudo()
        if not Config.is_enabled:
            return

        Leave = self.env['hr.leave']
        Task = self.env['project.task']

        for rec in self:
            if not rec.user_id:
                continue

            # Get the related employee record
            employee = rec.user_id.employee_ids[:1]
            if not employee:
                continue

            # Check for overlapping approved leave
            overlapping_leave = Leave.search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'validate'),
                ('date_from', '<=', fields.Date.today()),
                ('date_to', '>=', fields.Date.today())
            ], limit=1)

            if overlapping_leave:
                msg = _('User %s is on leave from %s to %s.') % (
                    rec.user_id.name, overlapping_leave.date_from, overlapping_leave.date_to)
                if Config.behavior == 'block':
                    raise ValidationError(msg)
                else:
                    # Log warning in chatter if just warning
                    rec.message_post(body=msg)

            # Check for other active tasks
            other_task = Task.search([
                ('id', '!=', rec.id),
                ('user_id', '=', rec.user_id.id),
                ('stage_id.fold', '=', False)
            ], limit=1)

            if other_task:
                msg = _('User %s is currently assigned to task %s.') % (
                    rec.user_id.name, other_task.name)
                if Config.behavior == 'block':
                    raise ValidationError(msg)
                else:
                    rec.message_post(body=msg)
override_reason = fields.Text(string="Reason for Override")
