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
		{"label":"PO Number", "fieldname":"name","fieldtype":"Link",'options':"Purchase Order",  "align":"center","width":125},
		{"label":"Vendor",  "fieldname":"vendor_name","fieldtype":"data","width":100 },
		{"label":"Product", "fieldname":"product_name","fieldtype":"Data","align":"left","width":100},
		{"label":"PO Quantity", "fieldname":"po_quantity","fieldtype":"Float","align":"center","width":125},
		{"label":"Unit", "fieldname":"unit","fieldtype":"Data","width":75},
		{"label":"PO Amount", "fieldname":"total_amount","fieldtype":"Currency","align":"right","width":100},
		
		{"label":"SO Quantity", "fieldname":"so_quantity","fieldtype":"Float","align":"center","width":100},
		{"label":"SO Amount", "fieldname":"so_amount","fieldtype":"Currency","align":"right","width":100},
		
		{"label":"Remaining QTY", "fieldname":"remaining_quantity","fieldtype":"Float","align":"center","width":150},
		{"label":"Remaining Amt", "fieldname":"remaining_amount","fieldtype":"Currency","align":"right","width":150},
		
	]
 
 


 
def get_conditions(filters,group_filter=None):
	conditions = " b.docstatus=1 "

	
	start_date = filters.start_date
	end_date = filters.end_date
	
	if  start_date  and end_date:
		conditions += " AND posting_date between %(start_date)s and %(end_date)s" 

	if filters.get("product"):
		conditions += " AND product_code = %(product)s"

	if filters.get("vendor"):
		conditions += " AND b.vendor = %(vendor)s"
	
	if filters.get("delivery_district"):
		conditions += " AND district= %(delivery_district3)s"
 
 
	return conditions

def get_report_data(filters,parent_row_group=None,indent=0,group_filter=None):
	
	sql = """select
			b.name,
			b.posting_date,
			b.vendor_name,
			a.product_name,
			a.unit,
			a.quantity as po_quantity,
			a.total_amount,
			a.delivered_quantity as so_quantity,
			a.delivered_price * a.delivered_quantity as so_amount,
			remaining_quantity as remaining_quantity,
			a.price * remaining_quantity as remaining_amount
		from `tabPurchase Order Product` a 
		inner join `tabPurchase Order` b on b.name = a.parent 
		where
			{}
		
	""".format(get_conditions(filters,group_filter))	
	 
	data = frappe.db.sql(sql,filters, as_dict=1)

	return data
 
 