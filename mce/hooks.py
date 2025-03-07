app_name = "mce"
app_title = "MCE"
app_publisher = "MCE"
app_description = "MCE"
app_email = "info@mce.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "mce",
# 		"logo": "/assets/mce/logo.png",
# 		"title": "MCE",
# 		"route": "/mce",
# 		"has_permission": "mce.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mce/css/mce.css"
# app_include_js = "/assets/mce/js/mce.js"

# include js, css files in header of web template
# web_include_css = "/assets/mce/css/mce.css"
# web_include_js = "/assets/mce/js/mce.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mce/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mce/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mce.utils.jinja_methods",
# 	"filters": "mce.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mce.install.before_install"
# after_install = "mce.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mce.uninstall.before_uninstall"
# after_uninstall = "mce.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mce.utils.before_app_install"
# after_app_install = "mce.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mce.utils.before_app_uninstall"
# after_app_uninstall = "mce.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mce.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Terms and Conditions": {
        "validate": "mce.custom.terms_and_conditions.terms_and_conditions.validate"
    }, 
    "Purchase Order": {
        "validate": "mce.custom.purchase_order.purchase_order.validate", 
        "on_submit" : "mce.custom.purchase_order.purchase_order.on_submit",
    }, 
    "Purchase Invoice":{
        "validate": "mce.custom.purchase_invoice.purchase_invoice.validate", 
        "on_submit" : "mce.custom.purchase_invoice.purchase_invoice.on_submit",
    }
}
doctype_js = {
    "Purchase Order": "custom/purchase_order/purchase_order.js",
    "Purchase Invoice": "custom/purchase_invoice/purchase_invoice.js",
    "Purchase Receipt": "custom/purchase_receipt/purchase_receipt.js",
    "Blanket Order": "custom/blanket_order/blanket_order.js",
    "Terms and Conditions" : "custom/terms_and_conditions/terms_and_conditions.js"
 }
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mce.tasks.all"
# 	],
# 	"daily": [
# 		"mce.tasks.daily"
# 	],
# 	"hourly": [
# 		"mce.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mce.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mce.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "mce.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mce.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mce.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mce.utils.before_request"]
# after_request = ["mce.utils.after_request"]

# Job Events
# ----------
# before_job = ["mce.utils.before_job"]
# after_job = ["mce.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mce.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                "Terms and Conditions-custom_section_break_jc7iz",
                "Terms and Conditions-custom_accounts",
                "Terms and Conditions-custom_column_break_xpab8",
                "Terms and Conditions-custom_has_accounting_effect",
                "Terms and Conditions-custom_blanket_order_term",
                "Blanket Order-custom_terms_details",
                "Blanket Order-custom_term", 
                "Blanket Order-custom_section_break_p9hva", 
                "Blanket Order-custom_fines",
                "Purchase Order-custom_blanket_order",
                "Purchase Order-custom_total_debit",
                "Purchase Order-custom_column_break_z6s93",
                "Purchase Order-custom_total_credit", 
                "Purchase Order-custom_section_break_luyq9", 
                "Purchase Order-custom_section_break_9d9gg",
                "Purchase Order-custom_term", 
                "Purchase Receipt-custom_section_break_nmslc",
                "Purchase Receipt-custom_fines",
                "Purchase Invoice-custom_section_break_s76tb",
                "Purchase Invoice-custom_fines",
                "Purchase Invoice-custom_section_break_kxewz",
                "Purchase Invoice-custom_column_break_ckoy8",
                "Purchase Invoice-custom_column_break_0ax76",
                "Purchase Invoice-custom_total_fines"
            ]
        ]
    ]}
]