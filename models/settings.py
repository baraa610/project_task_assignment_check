# models/settings.py
from odoo import models, fields

class ProjectPlanningSyncSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    delete_slot_behavior = fields.Selection(
        [('unlink', 'Delete Slot on Task Deletion'),
         ('remove_link', 'Just Remove Link')],
        string="Task Deletion Behavior",
        default='unlink',
    )
