// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
	refresh(frm) {
        if(!frm.doc.__islocal){
			 
			frm.call({
				method: 'get_summary',
				doc:frm.doc,
				callback:function(r){
					
					if(r.message){
						const d = r.message;
					 
						frm.dashboard.add_indicator(__("MTD PO Qty: {0}",[d.mtd_po_qty]) ,"blue");
						frm.dashboard.add_indicator(__("MTD PO Amt: {0}",[format_currency(d.mtd_po_amount)]) ,"blue");
                        
						frm.dashboard.add_indicator(__("MTD SO Qty: {0}",[d.mtd_so_qty]) ,"green");
						frm.dashboard.add_indicator(__("MTD SO Amt: {0}",[format_currency(d.mtd_so_amount)]) ,"green");
                        
					 
						frm.dashboard.add_indicator(__("YTD PO Qty: {0}",[d.ytd_po_qty]) ,"blue");
						frm.dashboard.add_indicator(__("YTD PO Amt: {0}",[format_currency(d.ytd_po_amount)]) ,"blue");
                        
						frm.dashboard.add_indicator(__("YTD SO Qty: {0}",[d.ytd_so_qty]) ,"green");
						frm.dashboard.add_indicator(__("YTD SO Amt: {0}",[format_currency(d.ytd_so_amount)]) ,"green");
                        

					}
					
				},
				async: true,
			});
			
			
		}
	},
});
