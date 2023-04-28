// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Truck", {
	refresh(frm) {
        set_product_indicator(frm);
	},
});



function set_product_indicator(frm){
    if(frm.doc.__islocal)
			return;
 
    frm.call({
        method: 'get_summary',
        doc:frm.doc,
        callback:function(r){

            if(r.message){
                const d = r.message;

                    frm.dashboard.add_indicator(__("Total Amount: {0}",[format_currency(d.total_amount)]) ,"blue");
                    frm.dashboard.add_indicator(__("Total Paid: {0}",[format_currency(d.total_paid)]) ,"green");
                    frm.dashboard.add_indicator(__("Balance: {0}",[format_currency(d.balance)]) ,"red");
                
            }

        },
        async: true,
    });
}