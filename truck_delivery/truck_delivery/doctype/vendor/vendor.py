# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Vendor(Document):
	
	@frappe.whitelist()
	def get_vendor_purchase_summary(self):
		#total deposit
		deposit_data = frappe.db.sql("select coalesce(sum(amount),0) as   amount from `tabVendor Deposit` where docstatus=1 and vendor='{}'".format(self.name), as_dict=1)
		data_purchase = frappe.db.sql("select coalesce(sum(total_amount),0) as   amount from `tabPurchase Order` where docstatus=1 and vendor='{}'".format(self.name), as_dict=1)
		#data_purchase = frappe.db.sql("select coalesce(sum(total_amount),0) as   amount from `tabPurchase Order` where docstatus=1 and vendor='{}'".format(self.name), as_dict=1)
		sql ="select coalesce(sum(total_amount),0) as   amount from `tabRequest for Quotation` where docstatus=1 and vendor='{0}' and name not in (select request_for_quotation from `tabPurchase Order` where docstatus=1 and vendor='{0}')".format(self.name)
		data_pending_rfq = frappe.db.sql(sql,as_dict=1)


		return {
			"total_deposit":deposit_data[0]["amount"],
			"total_purchase":data_purchase[0]["amount"],
			"balance":deposit_data[0]["amount"] - data_purchase[0]["amount"],
			"forcasting":data_pending_rfq[0]["amount"]
		}
