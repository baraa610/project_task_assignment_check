from odoo.tests.common import TransactionCase

class TestProjectPlanningSync(TransactionCase):

    def test_create_task_creates_slot(self):
        task = self.env['project.task'].create({'name': 'Test Task'})
        self.assertTrue(task.planning_slot_id, "Planning slot not created")
        slot = task.planning_slot_id
        self.assertEqual(slot.name, task.name)
        self.assertEqual(slot.task_id, task)
