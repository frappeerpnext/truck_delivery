# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Quotation(Document):
	def validate(self):
		self.total_qty = sum(c.quantity for c in self.product)
		self.total_additional_cost = sum(c.additional_cost for c in self.product)
		self.total_cost = sum(c.total_cost for c in self.product)
		self.cost = sum(c.cost for c in self.product)
		self.total_selling_price = sum(c.selling_price for c in self.product)
		for p in self.product:
			if p.is_free == 0:
				p.selling_price = p.markup_amount + p.total_cost
			else:
				p.selling_price = 0

		if self.total_cost > self.total_selling_price:
			self.profit=0
			self.loss = self.total_selling_price - self.total_cost
		else:
			self.loss=0
			self.profit = self.total_selling_price -  self.total_cost

@frappe.whitelist()
def get_customer_quotations(start,end,province=None,customer_type=None,customer=None):
	filters = {
		'start_date': ['>=', start],
		'end_date': ['<=', end] ,
		'docstatus': ['=', 1] ,

	}
	if str(province) != 'None':
		filters['province'] = ['=', province]
  
	if str(customer_type) != 'None':
		filters['customer_type'] = ['=', customer_type]\
      
	if str(customer) != 'None':
		filters['customer'] = ['=', customer]

	quotations = frappe.db.get_list('Quotation',fields=['name as id','start_date as start','end_date as end','province','customer','creation','customer_name'],filters=filters)
	for r in quotations:
		r.resourceId=''
		r.resourceId= r.customer
		r.province= r.province
	
	return quotations
