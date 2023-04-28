// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transportation Billing", {
	refresh(frm) {
        if(!frm.doc.__islocal){
		 
		 
            const d = frm.doc;
               
               frm.dashboard.add_indicator(__("Total Amount: {0}",[format_currency(frm.doc.total_cost)]) ,"blue");
               frm.dashboard.add_indicator(__("Paid: {0}",[format_currency(frm.doc.total_payment)]) ,"green");
               frm.dashboard.add_indicator(__("Balance: {0}",[format_currency(frm.doc.balance)]) ,"red");
            

           }
           
        if(!frm.doc.__islocal){
            var iframe = document.createElement('iframe');
            iframe.height="1122";
            iframe.width="100%";
            iframe.style="border:none"
            iframe.src = '/printview?doctype=Customer%20Invoice&name=' + frm.doc.name +  '&format=' + frappe.get_meta("Transportation Billing").fields.find(r=>r.fieldname=='transpotation_bill_receipt').default + '&no_letterhead=1&settings=%7B%7D&_lang=en';
        
            document.getElementById('transpotation_bill_receipt').appendChild(iframe);
            
            var customer_invoice_frame = document.createElement('iframe');
            customer_invoice_frame.height="1122";
            customer_invoice_frame.width="100%";
            customer_invoice_frame.style="border:none"
            customer_invoice_frame.src = '/printview?doctype=Customer%20Invoice&name=' + frm.doc.name +  '&format=' + frappe.get_meta("Transportation Billing").fields.find(r=>r.fieldname=='customer_invoice').default + '&no_letterhead=1&settings=%7B%7D&_lang=en';
        
            document.getElementById('customer_invoice_frame').appendChild(customer_invoice_frame);

            
        }
	},
});
