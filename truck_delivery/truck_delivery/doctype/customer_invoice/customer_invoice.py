# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

from py_linq import Enumerable
import frappe
from frappe.model.document import Document
# import frappe.permissions
from frappe.utils.data import add_to_date, getdate,format_date



class CustomerInvoice(Document):
	def validate(self):
		for d in self.products:
			
			d.total_amount = (d.quantity or 1) * (d.price or 0)
			d.transportation_cost_backup = calculate_product_cost(self,d) or 0
			if d.adjust_cost ==0:
				d.transportation_cost = d.transportation_cost_backup

			d.total_transportation_cost = (d.transportation_cost or 0 ) * d.quantity

		self.total_quantity = Enumerable(self.products).sum(lambda x: x.quantity or 0)
		self.total_amount =  Enumerable(self.products).sum(lambda x: x.total_amount or 0)
		self.balance = self.total_amount - (self.total_paid or 0)
		
		#calculate transaptation cost
		self.total_transportation_cost =  Enumerable(self.products).sum(lambda x: x.total_transportation_cost or 0)
		
	def before_submit(self):
		for d in self.products:
			d.total_amount = (d.quantity or 1) * (d.price or 0)
			validate_quaitity_with_po(d)


	def on_submit(self):
		update_quantity_to_po(self)

		doc = frappe.get_doc(
		{
			"name": self.name,
			"document_number": self.name,
			"vendor": self.vendor,
			"vendor_name": self.vendor_name,
			"phone_number": self.phone_number,
			"posting_date": self.posting_date,
			"district": self.district,
			"truck": self.truck,
			"driver": self.driver,
			"driver_name": self.driver_name,
			"driver_number": self.driver_number,
			"customer": self.customer,
			"customer_name": self.customer_name,
			"customer_phone_number": self.customer_phone_number,
			"customer_province": self.customer_province,
			"customer_district": self.customer_district,
			"doctype": "Transportation Billing",
			"total_cost": self.total_transportation_cost,
			"total_payment":0,
			"balance": self.total_transportation_cost,
			"total_quantity":self.total_quantity
		}
		)
		doc.insert()
		current_date = getdate()
		last_start_date = add_to_date(format_date(current_date,"yyyy-mm-01"),months=-1)
		last_end_date = add_to_date(format_date(current_date,"yyyy-mm-01"),days=-1)
		current_start_date = format_date(current_date,"yyyy-mm-01")
		current_end_date = format_date(current_date,"yyyy-mm-dd")
		sql = """ Update `tabCustomer` 
  						set last_month_order = Coalesce((SELECT SUM(total_quantity) from `tabCustomer Invoice` where posting_date between '{1}' and '{2}' and customer = '{0}'),0),
  						current_order = Coalesce((SELECT SUM(total_quantity) from `tabCustomer Invoice` where posting_date between '{3}' and '{4}' and customer = '{0}'),0) 
             		where name = '{0}'""".format(self.customer,last_start_date,last_end_date,current_start_date,current_end_date)
		frappe.db.sql(sql)
		frappe.enqueue('truck_delivery.truck_delivery.doctype.customer_invoice.customer_invoice.update_actual_sale_qty_to_quotation_product',self=self)

	def on_cancel(self):
	
		update_quantity_to_po(self)
		frappe.db.sql("delete from `tabTransportation Billing` where name='{}'".format(self.name))


def update_quantity_to_po(self):
	for d in self.products:
		sql = "select  coalesce(sum(quantity),0) as quantity,coalesce(sum(total_amount),0) as amount from `tabCustomer Invoice Product` where purchase_order_product_id='{}' and docstatus=1".format(d.purchase_order_product_id)
		data = frappe.db.sql(sql,as_dict=1)
		invoiced_quantity = data[0]["quantity"]
		amount = data[0]["amount"]

		#update remaining qty
		sql = "update `tabPurchase Order Product` set delivered_quantity={0}, remaining_quantity=quantity-{0},delivered_price = {1}/{2} where name='{3}'".format(invoiced_quantity,amount,invoiced_quantity if invoiced_quantity>0 else 1,d.purchase_order_product_id)
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
 
	# if (total_invoiced_quantity or 0)  + (row.quantity or 0) > (total_purchase_quantity or 0):
	# 	frappe.throw("Invoice quantity can not greater than purchase quantity at row {}".format(row.idx))
	


def calculate_product_cost(self,row):
	#get cost from range

	sql = "select cost from `tabTransportation Quantity Cost` where truck='{0}' and product='{1}' and district='{2}' and '{3}' between start_date and end_date and {4} between min_quantity and max_quantity and docstatus=1"
 
	sql = sql.format(self.truck, row.product_code,self.district,self.posting_date, row.quantity)
	data = frappe.db.sql(sql,as_dict=1)

	if data:
		return data[0]["cost"]
	else:
		#get cost from transportation cost
		sql = "select cost from `tabTransportation Cost` where truck='{0}' and product='{1}' and district='{2}' and '{3}' between start_date and end_date and docstatus=1"
	
		sql = sql.format(self.truck, row.product_code,self.district,self.posting_date)
		 
		data = frappe.db.sql(sql,as_dict=1)
		if data:
			return data[0]["cost"]
		else:
			return 0

def update_actual_sale_qty_to_quotation_product(self):
	if self.quotation:
		sql = """
  				update  `tabCustomer Quotation Product` a 
				INNER JOIN `tabQuotation` b ON b.name = a.parent
				INNER JOIN `tabCustomer Invoice` c ON c.quotation = b.name  
				INNER Join `tabCustomer Invoice Product` d ON c.name = d.parent and a.product=d.product_code
				set a.actual_quantity = d.quantity
				WHERE c.name = '{}' and c.posting_date between a.start_date and a.end_rate
			""".format(self.name)
		frappe.db.sql(sql)


@frappe.whitelist()
def update_customer_order():
	sql = """
		UPDATE `tabCustomer` AS c
		JOIN (
			SELECT customer, SUM(total_quantity) AS total_quantity
			FROM `tabCustomer Invoice`
			WHERE posting_date BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') AND LAST_DAY(NOW())
			GROUP BY customer
		) AS so ON c.name = so.customer
		SET c.current_order = so.total_quantity;
	"""
	frappe.db.sql(sql)

  
