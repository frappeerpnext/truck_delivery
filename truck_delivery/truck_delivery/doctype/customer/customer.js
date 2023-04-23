// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

var iframe = document.createElement('iframe');
iframe.height="1122";
iframe.width="100%";
iframe.style="border:none"

frappe.ui.form.on("Customer", {
	refresh(frm) {
        if(!frm.doc.__islocal){
            iframe.src = '/printview?doctype=Customer&name=' + frm.doc.name +  '&format=' + frappe.get_meta("Customer").fields.find(r=>r.fieldname=='product_history').default + '&no_letterhead=1&settings=%7B%7D&_lang=en&view=ui&show_toolbar=0';
            document.getElementById('customer_purchase_product_history').appendChild(iframe);
        }
	},
    view_report(frm){

        let src = '/printview?doctype=Customer&name=' + frm.doc.name +  '&format=' + frappe.get_meta("Customer").fields.find(r=>r.fieldname=='product_history').default + '&no_letterhead=1&settings=%7B%7D&_lang=en&view=ui&show_toolbar=0';
        src = src + "&start_date=" + frm.doc.start_date +  "&end_date=" + frm.doc.end_date + "&product=" + (frm.doc.filter_product || '')
        
        iframe.contentWindow.location.replace(src)
      
        
    }
});
