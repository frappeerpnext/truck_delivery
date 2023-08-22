 
# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt
import frappe
from py_linq import Enumerable
from frappe.model.document import Document

class PurchaseOrder(Document):
	def validate(self):
		for d in self.products:
			d.total_amount = (d.quantity or 1) * (d.price or 0)
			d.remaining_quantity  = (d.quantity or 0)  -  (d.delivered_quantity or 0)

		self.total_quantity = Enumerable(self.products).sum(lambda x: x.quantity or 0)
		self.total_delivered_quantity = Enumerable(self.products).sum(lambda x: x.delivered_quantity or 0)
		self.total_remaining_quantity = Enumerable(self.products).sum(lambda x: x.remaining_quantity or 0)
		self.total_amount =  Enumerable(self.products).sum(lambda x: x.total_amount or 0)

	def on_submit(self):
		if self.request_for_quotation:
			data = frappe.db.sql("select count(name) as total_order from `tabPurchase Order` where docstatus=1 and request_for_quotation='{}'".format(self.request_for_quotation),as_dict=1)
			if data:
				frappe.db.set_value("Request for Quotation", self.request_for_quotation,"total_purchase_order", data[0]["total_order"])
			