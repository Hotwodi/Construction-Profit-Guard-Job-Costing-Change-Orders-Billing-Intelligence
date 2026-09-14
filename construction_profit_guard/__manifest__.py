{
    'name': 'Construction Profit Guard: Job Costing, Change Orders & Billing Intelligence',
    'version': '18.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered construction job costing, change orders, progress billing & compliance',
    'description': """
Construction Profit Guard
=========================

AI-powered construction project management with job costing, change orders,
progress billing (AIA-style), subcontractor compliance tracking, and intelligent
margin forecasting.

Key Features:
- Construction project tracking with budget vs. actuals
- Cost code management with overrun risk detection
- Job cost entries (PO, timesheet, vendor bill, inventory, manual)
- Change order lifecycle management
- Daily site logs with AI change-order flagging
- AIA-style progress billing with retention
- Subcontractor compliance monitoring (COI, insurance expiry)
- Commitment tracking (PO, subcontract, inventory transfer)
- AI margin forecasting and overrun risk scoring
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'license': 'LGPL-3',
    'price': 799.99,
    'currency': 'USD',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/cpg_project_views.xml',
        'views/cpg_cost_code_views.xml',
        'views/cpg_job_cost_entry_views.xml',
        'views/cpg_change_order_views.xml',
        'views/cpg_daily_site_log_views.xml',
        'views/cpg_progress_billing_views.xml',
        'views/cpg_subcontractor_compliance_views.xml',
        'views/cpg_commitment_views.xml',
        'views/cpg_menu.xml',
    ],
    'assets': {},
    'images': ['static/description/cover.png'],
}
