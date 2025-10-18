{
    'name': 'Task Assignment Monitor',
    'version': '17.0.1.0.0',
    'category': 'Project',
    'summary': 'Monitor task assignments and alert for uncovered tasks',
    'description': """

                                              Task Assignment Monitor
                                              ========================
                                              This module monitors task assignments and triggers alerts when:
                                              - Tasks are assigned to employees on approved leave
                                              - Tasks are assigned to employees already busy with other tasks

                                              Features:
                                              ---------
                                              * Real-time task assignment monitoring
                                              * Leave status integration
                                              * Workload calculation
                                              * In-app notifications for uncovered tasks
                                              * Visual availability indicators
                                              * Dashboard for uncovered tasks
                                          """,
    'author': 'Moahmed Hussein',
    'email': 'mhussein610@gmail.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'project',
        'hr_holidays',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/uncovered_task_views.xml',
        'data/mail_template_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'task_assignment_monitor/static/src/js/task_availability_widget.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
