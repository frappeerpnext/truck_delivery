# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

from py_linq import Enumerable
import frappe
from frappe.model.document import Document

class CustomerInvoice(Document):
	def validate(self):
		for d in self.products:
	
			d.total_amount = (d.quantity or 1) * (d.price or 0)
			calculate_product_cost(self,d)

		self.total_quantity = Enumerable(self.products).sum(lambda x: x.quantity or 0)
		self.total_amount =  Enumerable(self.products).sum(lambda x: x.total_amount or 0)
		#calculate transaptation cost


	def before_submit(self):
		for d in self.products:
			d.total_amount = (d.quantity or 1) * (d.price or 0)
			validate_quaitity_with_po(d)

	def on_submit(self):
		update_quantity_to_po(self)

	def on_cancel(self):
	
		update_quantity_to_po(self)

def update_quantity_to_po(self):
	for d in self.products:
		sql = "select  coalesce(sum(quantity),0) as quantity from `tabCustomer Invoice Product` where purchase_order_product_id='{}' and docstatus=1".format(d.purchase_order_product_id)
		data = frappe.db.sql(sql,as_dict=1)
		invoiced_quantity = data[0]["quantity"]
		#update remaining qty
		sql = "update `tabPurchase Order Product` set delivered_quantity={0}, remaining_quantity=quantity-{0} where name='{1}'".format(invoiced_quantity,d.purchase_order_product_id)
		frappe.db.sql(sql)
	
	#update total deliver and remaining to main doc type Purchase Order
	frappe.db.commit()
	#get sum data
	sql = "select coalesce(sum(delivered_quantity),0) as deliverd_quantity,coalesce(sum(remaining_quantity),0) as remaining_quantity from `tabPurchase Order Product` where parent='{}' and docstatus=1".format(self.purchase_order)
	data = frappe.db.sql(sql,as_dict=1)
	
	#update to main table
	sql = "update `tabPurchase Order` set total_delivered_quantity={0},total_remaining_quantity={1} where name='{2}'".format(data[0]["deliverd_quantity"],data[0]["remaining_quantity"], self.purchase_order)

	frappe.db.sql(sql)





def validate_quaitity_with_po(row):
	data  = frappe.db.sql("select coalesce(sum(quantity),0) as quantity from `tabPurchase Order Product` where name='{}'".format(row.purchase_order_product_id),as_dict=1)
	total_purchase_quantity =  data[0]["quantity"]
	data  = frappe.db.sql("select coalesce(sum(quantity),0) as quantity from `tabCustomer Invoice Product` where purchase_order_product_id='{}' and docstatus = 1".format(row.purchase_order_product_id),as_dict=1)
	total_invoiced_quantity  =  data[0]["quantity"]
 
	if (total_invoiced_quantity or 0)  + (row.quantity or 0) > (total_purchase_quantity or 0):
		frappe.throw("Invoice quantity can not greater than purchase quantity at row {}".format(row.idx))
	


def calculate_product_cost(self,row):
	#get cost from range
	sql = "select cost from `tabTransportation Quantity Cost` where truck='{0}' and product='{1}' and district='{2}' and '{3}' between start_date and end_date and {4} between min_quantity and max_quantity and docstatus=1"
	sql = sql.format(self.truck, row.product,self.district,self.create_date, row.quantity)
	frappe.throw(sql)