from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date


class ProjectTask(models.Model):
    _inherit = 'project.task2'

    assignee_availability_status = fields.Selection([
        ('available', 'Available'),
        ('on_leave', 'On Leave'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ], string='Assignee Status', compute='_compute_assignee_availability')

    assignee_workload = fields.Integer(
        string='Active Tasks Count',
        compute='_compute_assignee_availability'
    )

    is_uncovered = fields.Boolean(
        string='Is Uncovered',
        compute='_compute_assignee_availability'
    )

    @api.depends('user_ids', 'user_ids.employee_id')
    def _compute_assignee_availability(self):
        """Compute availability status of assigned users"""
        for task in self:
            if not task.user_ids:
                task.assignee_availability_status = 'available'
                task.assignee_workload = 0
                task.is_uncovered = False
                continue

            user = task.user_ids[0] if task.user_ids else False

            if not user:
                task.assignee_availability_status = 'available'
                task.assignee_workload = 0
                task.is_uncovered = False
                continue

            is_on_leave = task._check_user_on_leave(user)
            active_tasks_count = task._get_user_active_tasks(user)

            task.assignee_workload = active_tasks_count

            if is_on_leave:
                task.assignee_availability_status = 'on_leave'
                task.is_uncovered = True
            elif active_tasks_count >= 3:
                task.assignee_availability_status = 'busy'
                task.is_uncovered = True
            else:
                task.assignee_availability_status = 'available'
                task.is_uncovered = False

    def _check_user_on_leave(self, user):
        """Check if user is currently on approved leave"""
        if not user.employee_id:
            return False

        today = fields.Date.today()
        leave = self.env['hr.leave'].search([
            ('employee_id', '=', user.employee_id.id),
            ('state', '=', 'validate'),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
        ], limit=1)

        return bool(leave)

    def _get_user_active_tasks(self, user):
        """Get count of active tasks assigned to user (excluding this task)"""
        domain = [
            ('user_ids', 'in', user.id),
            ('stage_id.fold', '=', False),
        ]
        if self.id:
            domain.append(('id', '!=', self.id))

        active_tasks = self.env['project.task'].search_count(domain)
        return active_tasks

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to check availability and create alerts"""
        tasks = super(ProjectTask, self).create(vals_list)
        for task in tasks:
            if task.is_uncovered:
                self._create_uncovered_alert(task)
                self._send_notification(task)
        return tasks

    def write(self, vals):
        """Override write to check availability when assignee changes"""
        result = super(ProjectTask, self).write(vals)

        if 'user_ids' in vals:
            for task in self:
                if task.is_uncovered:
                    self._create_uncovered_alert(task)
                    self._send_notification(task)

        return result

    def _create_uncovered_alert(self, task):
        """Create an uncovered task alert record"""
        alert = self.env['uncovered.task.alert'].search([
            ('task_id', '=', task.id),
            ('state', '=', 'active'),
        ], limit=1)

        if not alert:
            reason = ''
            if task.assignee_availability_status == 'on_leave':
                reason = _('Assigned user is on approved leave')
            elif task.assignee_availability_status == 'busy':
                reason = _('Assigned user is busy with %d other active tasks') % task.assignee_workload

            self.env['uncovered.task.alert'].create({
                'task_id': task.id,
                'assigned_user_id': task.user_ids[0].id if task.user_ids else False,
                'reason': reason,
                'availability_status': task.assignee_availability_status,
            })

    def _send_notification(self, task):
        """Send in-app notification for uncovered task"""
        if not task.user_ids:
            return

        user = task.user_ids[0]
        project_manager = task.project_id.user_id

        reason_msg = ''
        if task.assignee_availability_status == 'on_leave':
            reason_msg = _('is on approved leave')
        elif task.assignee_availability_status == 'busy':
            reason_msg = _('is already busy with %d active tasks') % task.assignee_workload

        message = _(
            'Alert: Task "%s" assigned to %s who %s. This task may be uncovered.'
        ) % (task.name, user.name, reason_msg)

        notification_ids = []

        if project_manager:
            notification_ids.append((0, 0, {
                'res_partner_id': project_manager.partner_id.id,
                'notification_type': 'inbox',
            }))

        task.message_post(
            body=message,
            subject=_('Uncovered Task Alert'),
            message_type='notification',
            subtype_xmlid='mail.mt_note',
            notification_ids=notification_ids,
        )

    def action_open_uncovered_alerts(self):
        """Open uncovered task alerts related to this task"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Uncovered Task Alerts'),
            'res_model': 'uncovered.task.alert',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
        }
