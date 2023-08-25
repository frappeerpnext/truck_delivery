# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.data import add_to_date, getdate
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
		total_cost_quotation = sum(c.total_cost_quotation for c in self.product) or 0
		total_selling_quotation_price = sum(c.total_selling_quotation_price for c in self.product) or 0
		if total_cost_quotation> total_selling_quotation_price:
			self.profit=0
			self.loss = total_cost_quotation - total_selling_quotation_price
		else:
			self.loss=0
			self.profit = total_selling_quotation_price - total_cost_quotation
   
	def after_insert(self):
		start_date = getdate(self.start_date)
		while start_date <= getdate(self.end_date) :
			frappe.get_doc({'doctype':'Quotation Date','date':start_date,'quotation_number':self.name,'customer':self.customer,'customer_name':self.customer_name,'customer_type':self.customer_type}).insert()
			
			start_date=add_to_date(start_date,days=1)
		frappe.db.commit()
	
	def on_cancel(self):
		sql = """ delete from `tabQuotation Date` where quotation_number ='{}' """.format(self.name)
		frappe.db.sql(sql,as_dict=1)

	def after_delete(self):
		sql = """ delete from `tabQuotation Date` where quotation_number ='{}' """.format(self.name)
		frappe.db.sql(sql,as_dict=1)

@frappe.whitelist()
def get_customer_quotations(start,end,customer_type=None,customer=None):
	if customer_type:
		customer_type = "'"+customer_type+"'"
	if customer :
		customer = "'"+customer+"'"
	sql=""" 
 		select
   			customer as resourceId,
			a.name as id,
			a.start_date as start,
			a.end_date as end,
			a.name as title,
   			IF(a.docstatus=1,"#007bff","#efefef") as backgroundColor,
			IF(a.docstatus=1,"white","#18181a") as textColor, 
			IF(a.docstatus=1,"#007bff","#efefef") as borderColor,
			b.current_order,
			b.last_month_order
        from `tabQuotation` a
        inner join `tabCustomer` b on a.customer = b.name
        where 
        	a.name in (select distinct quotation_number from `tabQuotation Date` where date between '{0}' and '{1}' and customer = {2} and customer_type = {3}) and
    		a.customer = {2}  and a.customer_type = a.{3}""".format(getdate(start),getdate(end),customer or 'customer',customer_type or 'customer_type')
	quotations = frappe.db.sql(sql,as_dict=1)
	return quotations
