{
    'name': 'HR Employee Form 16',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Form 16 Generation for Employees',
    'license': 'AGPL-3',
    'description': """
    This module extends the HR Employee module to generate Form 16 certificates for employees.
    Features:
    - Form 16 template with proper formatting
    - Quarterly TDS data management
    - Salary and tax calculation details
    - Chapter VI-A deductions support
    - Print button integration
    """,
    'author': 'Zigma Technologies',
    'website': 'https://www.yourcompany.com',
    'depends': ['hr', 'base'],
    'external_dependencies': {'python': ['num2words']},
    'data': [
        'security/ir.model.access.csv',
        # 'views/hr_employee_views.xml',
        'views/employee_views.xml',
        'reports/form16_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
