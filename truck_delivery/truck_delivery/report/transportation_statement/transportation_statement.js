// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt
/* eslint-disable */
 
frappe.query_reports["Transportation Statement"] = {
	
	"filters": [
	
		
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			
			 
		},
		
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
			
		},

		{
			fieldname: "truck",
			label: __("Truck"),
			fieldtype: "Link",
			options:"Truck"
			 
		},

		{
			fieldname: "delivery_district",
			label: __("Delivery District"),
			fieldtype: "Link",
			options:"District"
			 
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

 