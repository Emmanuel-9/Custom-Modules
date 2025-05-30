# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey leads generation",
    "summary": "Generate CRM leads/opportunities from surveys",
    "version": "17.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": [
        "survey",
        "crm",
        "crm_iap_enrich",
        "sale_crm",
        "enhanced_survey_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/survey_crm_demo.xml",
        "data/mail_template.xml",
        "views/survey_survey_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/crm_lead_views.xml",
    ],
    "application": True,
    "assets": {
        "web.assets_tests": [
            "/survey_crm_generation/static/tests/survey_crm_generation_tour.js",
        ],
    },
}
