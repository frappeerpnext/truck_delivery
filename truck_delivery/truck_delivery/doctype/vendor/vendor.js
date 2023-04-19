// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor", {
	refresh(frm) {
        if(!frm.doc.__islocal){
			 
			frm.call({
				method: 'get_vendor_purchase_summary',
				doc:frm.doc,
				callback:function(r){
					
					if(r.message){
						const d = r.message;
					 
						frm.dashboard.add_indicator(__("Total Deposit: {0}",[format_currency(d.total_deposit)]) ,"blue");
						frm.dashboard.add_indicator(__("Purchased: {0}",[format_currency(d.total_purchase)]) ,"blue");
						frm.dashboard.add_indicator(__("Outstanding: {0}",[format_currency(d.balance)]) ,"green");
						frm.dashboard.add_indicator(__("Forcasting Balance: {0}",[format_currency(d.forcasting)]) ,"orange");
						if (d.forcasting - d.balance> 0) frm.dashboard.add_indicator(__("RFD: {0}",[format_currency(d.forcasting - d.balance )]) ,"red");

					}
					
				},
				async: true,
			});
			
			
		}
	},
});
