# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Payments(Document):
	def on_submit(self):
		data = frappe.db.sql("select coalesce(sum(payment_amount),0) as amount from `tabPayments` where customer_invoice='{}'".format(self.customer_invoice),as_dict=1)
		amount = 0
		if data:
			amount = data[0]["amount"]
		
		frappe.db.sql("update `tabCustomer Invoice` set total_paid={0}, balance=total_amount - {0} where name='{1}'".format(amount, self.customer_invoice ) )
