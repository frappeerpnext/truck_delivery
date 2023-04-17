# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt
import frappe
from py_linq import Enumerable
from frappe.model.document import Document

class RequestforQuotation(Document):
	def validate(self):
		for d in self.products:
	
			d.total_amount = (d.quantity or 1) * (d.price or 0)

		self.total_quantity = Enumerable(self.products).sum(lambda x: x.quantity or 0)
		self.total_amount =  Enumerable(self.products).sum(lambda x: x.total_amount or 0)
