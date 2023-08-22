import frappe

@frappe.whitelist()
def get_quotation_product():
    frappe.db.get_all("Customer Quotation Product")

@frappe.whitelist()
def get_resourses(s):
    return 'hello'