from . import __version__ as app_version

app_name = "truck_delivery"
app_title = "Truck delivery"
app_publisher = "tes pheakdey"
app_description = "truck deliver"
app_email = "pheakdey.micronet@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/truck_delivery/css/truck_delivery.css"
# app_include_js = "/assets/truck_delivery/js/truck_delivery.js"

# include js, css files in header of web template
# web_include_css = "/assets/truck_delivery/css/truck_delivery.css"
# web_include_js = "/assets/truck_delivery/js/truck_delivery.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "truck_delivery/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "truck_delivery.utils.jinja_methods",
#	"filters": "truck_delivery.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "truck_delivery.install.before_install"
# after_install = "truck_delivery.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "truck_delivery.uninstall.before_uninstall"
# after_uninstall = "truck_delivery.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "truck_delivery.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
		"0 * * * *": [
			"truck_delivery.truck_delivery.doctype.customer_invoice.customer_invoice.update_customer_order",
		],
	},
    
#	"all": [
#		"truck_delivery.tasks.all"
#	],
#	"daily": [
#		"truck_delivery.tasks.daily"
#	],
#	"hourly": [
#		"truck_delivery.tasks.hourly"
#	],
#	"weekly": [
#		"truck_delivery.tasks.weekly"
#	],
#	"monthly": [
#		"truck_delivery.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "truck_delivery.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "truck_delivery.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "truck_delivery.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"truck_delivery.auth.validate"
# ]

website_route_rules = [{'from_route': '/scheme/<path:app_path>', 'to_route': 'scheme'},]

 