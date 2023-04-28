# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Truck(Document):
	@frappe.whitelist()
	def get_summary(self):
		sql  = "select sum(total_cost) as total_cost, sum(total_payment) as total_payment from `tabTransportation Billing` where truck='{}'"
		data = frappe.db.sql(sql.format(self.name), as_dict=1)
		if data:
			return {
				"total_amount":data[0]["total_cost"] or 0,
				"total_paid":data[0]["total_payment"] or 0,
				"balance":(data[0]["total_cost"] or 0) + (data[0]["total_payment"] or 0)
			}
		else:
			return {
				"total_amount":0,
				"total_paid":0,
				"balance":0
			}	