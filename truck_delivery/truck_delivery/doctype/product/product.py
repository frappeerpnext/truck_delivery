# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document

class Product(Document):
	@frappe.whitelist()
	def get_summary(self):
		#get mtd
		end_date =datetime.datetime.now()
		
		start_date =  datetime.date(end_date.year, end_date.month, 1)
		ytd_start_date =  datetime.date(end_date.year, 1, 1)
		end_date = end_date.strftime('%Y-%m-%d')

		
	 
		
		sql = "select coalesce(sum(a.quantity),0) as quantity, coalesce(sum(a.total_amount),0) as total_amount from `tabPurchase Order Product` a inner join `tabPurchase Order` b on b.name = a.parent where product_code='{}' and b.posting_date between '{}' and '{}' and b.docstatus=1".format(self.name, start_date,end_date)
		mtd_po = frappe.db.sql(sql, as_dict=1)
		
		sql = "select coalesce(sum(a.quantity),0) as quantity, coalesce(sum(a.total_amount),0) as total_amount from `tabCustomer Invoice Product` a inner join `tabCustomer Invoice` b on b.name = a.parent where product_code='{}' and b.posting_date between '{}' and '{}' and b.docstatus=1".format(self.name, start_date,end_date)
		mtd_so= frappe.db.sql(sql, as_dict=1)
		start_date = ytd_start_date
			
		sql = "select coalesce(sum(a.quantity),0) as quantity, coalesce(sum(a.total_amount),0) as total_amount from `tabPurchase Order Product` a inner join `tabPurchase Order` b on b.name = a.parent where product_code='{}' and b.posting_date between '{}' and '{}' and b.docstatus=1".format(self.name, start_date,end_date)
		ytd_po = frappe.db.sql(sql, as_dict=1)

		sql = "select coalesce(sum(a.quantity),0) as quantity, coalesce(sum(a.total_amount),0) as total_amount from `tabCustomer Invoice Product` a inner join `tabCustomer Invoice` b on b.name = a.parent where product_code='{}' and b.posting_date between '{}' and '{}' and b.docstatus=1".format(self.name, start_date,end_date)
		ytd_so= frappe.db.sql(sql, as_dict=1)
		

		return {
			"mtd_po_qty":mtd_po[0]["quantity"],
			"mtd_po_amount":mtd_po[0]["total_amount"],
			
			"mtd_so_qty":mtd_so[0]["quantity"],
			"mtd_so_amount":mtd_so[0]["total_amount"],
			
			"ytd_po_qty":ytd_po[0]["quantity"],
			"yetd_po_amount":ytd_po[0]["total_amount"],
			
			"ytd_so_qty":ytd_so[0]["quantity"],
			"ytd_so_amount":ytd_so[0]["total_amount"]

		} 


