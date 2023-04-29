import frappe
from frappe.utils import date_diff,today 
from frappe.utils.data import strip
from frappe import _
from py_linq import Enumerable

def execute(filters=None): 
 
 
	#run this to update parent_product_group in table sales invoice item

	report_data = []

	
	report_data = get_report_data(filters) 

	return get_columns(filters), report_data, None, None, None,False
 
# def validate(filters):
# 	pass
 
def get_columns(filters):
	return [
		{"label":"Date", "fieldname":"posting_date","fieldtype":"Date",  "align":"center"},
		{"label":"Truck",  "fieldname":"truck","fieldtype":"data","width":100 },
		{"label":"District", "fieldname":"delivery_district","fieldtype":"Data","align":"left","width":100},
		{"label":"Customer", "fieldname":"customer_name","fieldtype":"Data","align":"left","width":150},
		{"label":"Driver", "fieldname":"driver_name","fieldtype":"Data","align":"left","width":150},
		{"label":"Total Cost", "fieldname":"total_cost","fieldtype":"Currency","align":"right","width":100},
		{"label":"Total Payment", "fieldname":"total_payment","fieldtype":"Currency","align":"right","width":100},
		{"label":"Balance", "fieldname":"balance","fieldtype":"Currency","align":"right","width":100},
		
	]
 
 


 
def get_conditions(filters,group_filter=None):
	conditions = " 1=1 "

	
	start_date = filters.start_date
	end_date = filters.end_date
	
	if  start_date  and end_date:
		conditions += " AND posting_date between %(start_date)s and %(end_date)s" 

	if filters.get("truck"):
		conditions += " AND truck = %(truck)s"
	
	if filters.get("delivery_district"):
		conditions += " AND district= %(delivery_district3)s"
 
 
	return conditions

def get_report_data(filters,parent_row_group=None,indent=0,group_filter=None):
	
	sql = """select
			posting_date,
			truck,
			district as delivery_district, 
			customer_name,
			driver_name,
			total_cost ,
			total_payment ,
			balance
		from `tabTransportation Billing` 
		where
			{}
		
	""".format(get_conditions(filters,group_filter))	
	 
	data = frappe.db.sql(sql,filters, as_dict=1)

	return data
 
 