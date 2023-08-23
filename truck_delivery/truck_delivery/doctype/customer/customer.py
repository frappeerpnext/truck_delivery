# Copyright (c) 2023, tes pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Customer(Document):
	pass
@frappe.whitelist()
def get_resourses(district=None,customer=None):
	if str(district) != 'None':
		districts = frappe.db.get_all('District',fields=['name as id','province','name'],filters={"name":district})
	else:
		districts = frappe.db.get_all('District',fields=['name as id','province','name'])
	
	for dis in districts:
		dis.children=[]
		dis.title=dis.name
		if customer:
			customers = frappe.db.get_list('Customer',filters={"district":dis.id,"name":customer},fields=['name as id','customer_name as title','customer_type','province'])
			
		else:
			customers = frappe.db.get_list('Customer',filters={"district":dis.id},fields=['name as id','customer_name as title','customer_type','province'])
		dis.children = customers
	filtered_data = [item for item in districts if item["children"]]
	return filtered_data
