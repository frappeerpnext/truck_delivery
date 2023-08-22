# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Customer(Document):
	pass
@frappe.whitelist()
def get_resourses():
	districts = frappe.db.get_all('District',fields=['name as id','name as title'])
	
	for dis in districts:
		dis.children=[]
		customers = frappe.db.get_all('Customer',filters={"district":dis.id},fields=['name as id','customer_name as title','customer_type','province'])
		dis.children = customers
	return districts
