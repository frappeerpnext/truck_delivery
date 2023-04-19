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
		if self.costs:
			min_cost = min(self.costs, key=lambda x:x.cost)
			max_cost = max(self.costs, key=lambda x:x.cost)

			self.min_cost = min_cost.cost or self.cost
			self.max_cost = max_cost.cost or self.cost
		else:
			self.min_cost =0
			self.max_cost =0
