from odoo import models, fields, api
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    planning_slot_id = fields.Many2one('planning.slot', string='Planning Slot', readonly=True)

    @api.model
    def create(self, vals):
        task = super().create(vals)
        task._sync_to_planning_slot()
        return task

    def write(self, vals):
        res = super().write(vals)
        self._sync_to_planning_slot(update=True)
        return res

    def unlink(self):
        for task in self:
            if task.planning_slot_id:
                config = self.env['ir.config_parameter'].sudo().get_param('project_planning_sync.delete_slot', default='unlink')
                try:
                    if config == 'unlink':
                        task.planning_slot_id.sudo().unlink()
                    elif config == 'remove_link':
                        task.planning_slot_id.write({'task_id': False})
                except Exception as e:
                    _logger.warning("Failed to delete or unlink planning slot for task %s: %s", task.id, e)
        return super().unlink()

    def _sync_to_planning_slot(self, update=False):
        """Sync task to planning slot"""
        PlanningSlot = self.env['planning.slot']
        for task in self:
            # Determine if slot exists
            slot = task.planning_slot_id
            slot_vals = {
                'name': task.name,
                'user_id': task.user_id.id if task.user_id else False,
                'project_id': task.project_id.id if task.project_id else False,
                'task_id': task.id,
                'start_datetime': task.date_start or fields.Datetime.now(),
                'end_datetime': task.date_deadline,
                'description': task.description,
            }
            if slot:
                slot.write(slot_vals)
            else:
                # Create new slot
                new_slot = PlanningSlot.sudo().create(slot_vals)
                task.planning_slot_id = new_slot.id
