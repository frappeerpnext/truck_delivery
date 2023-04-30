// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt
/* eslint-disable */
 
frappe.query_reports["Product Purchase VS Sale"] = {
	
	"filters": [
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			"reqd": 1
			
			 
		},
		
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
			"reqd": 1
		},
		{
			fieldname: "vendor",
			label: __("Vendor"),
			fieldtype: "Link",
			options:"Vendor"
			 
		},
		{
			fieldname: "product",
			label: __("Product"),
			fieldtype: "Link",
			options:"Product"
			 
		},

	],
	// "formatter": function(value, row, column, data, default_formatter) {
	
	// 	value = default_formatter(value, row, column, data);

	// 	if (data && data.is_group==1) {
	// 		value = $(`<span>${value}</span>`);

	// 		var $value = $(value).css("font-weight", "bold");
			

	// 		value = $value.wrap("<p></p>").parent().html();
	// 	}
		
	// 	return value;
	// },
	
};

 