from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class TestTaskAssignment(TransactionCase):

    def setUp(self):
        super(TestTaskAssignment, self).setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.user = self.env['res.users'].create({'name': 'Test User', 'login': 'test_user'})
        self.employee.user_id = self.user.id
        self.project = self.env['project.project'].create({'name': 'Test Project'})
        self.config = self.env['project.task.assignment.config'].create({
            'is_enabled': True,
            'behavior': 'block'
        })

    def test_user_on_leave_block(self):
        leave = self.env['hr.leave'].create({
            'name': 'Vacation',
            'employee_id': self.employee.id,
            'request_date_from': date.today(),
            'request_date_to': date.today() + timedelta(days=2),
            'state': 'validate',
        })
        task = self.env['project.task'].create({
            'name': 'Test Task Leave',
            'project_id': self.project.id,
        })
        with self.assertRaises(ValidationError):
            task.user_id = self.user

    def test_user_busy_task_block(self):
        task1 = self.env['project.task'].create({
            'name': 'Active Task',
            'project_id': self.project.id,
            'user_id': self.user.id,
        })
        task2 = self.env['project.task'].create({
            'name': 'New Task',
            'project_id': self.project.id,
        })
        with self.assertRaises(ValidationError):
            task2.user_id = self.user
