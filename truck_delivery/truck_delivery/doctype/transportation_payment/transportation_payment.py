# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransportationPayment(Document):
	def on_submit(self):
		data = frappe.db.sql("select coalesce(sum(payment_amount),0) as amount from `tabTransportation Payment` where transportation_invoice='{}'".format(self.transportation_invoice),as_dict=1)
		amount = 0
		if data:
			amount = data[0]["amount"]
		
		frappe.db.sql("update `tabTransportation Billing` set total_payment={0}, balance=total_cost - {0} where name='{1}'".format(amount, self.transportation_invoice ) )

