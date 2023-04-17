# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransportationCost(Document):
	def validate(self):
		for d in self.costs:
			d.district = self.district
			d.product= self.product
			d.truck = self.truck
			d.start_date = self.start_date
			d.end_date = self.end_date
