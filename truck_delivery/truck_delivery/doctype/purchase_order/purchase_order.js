frappe.ui.form.on('Purchase Order', {
    
    refresh: function (frm) {
        if(!frm.doc.__islocal){
		 
		 
					 const d = frm.doc;
						frm.dashboard.add_indicator(__("Total Quantity: {0}",[d.total_quantity]) ,"blue");
						frm.dashboard.add_indicator(__("Delivered Qty: {0}",[d.total_delivered_quantity]) ,"orange");
						frm.dashboard.add_indicator(__("Remaining Qty: {0}",[d.total_remaining_quantity]) ,"red");
						

					}
					
			 
			
		 
    },
    onload: function (frm) {
       
        setTimeout(function () {
           
            if (frm.doc.request_for_quotation) {
             
             
                if (frm.doc.__islocal) {
                   
                    const data = frappe.get_doc("Request for Quotation", frm.doc.request_for_quotation)
                    
                    data.products.forEach(r => {
                    
                        var row = frappe.model.add_child(frm.doc, '', 'products');
                        
                        row.product_code = r.product_code;
                        row.product_name = r.product_name;
                        row.unit = r.unit;
                        row.quantity = r.quantity ;
                        row.price = r.price;
                        row.total_amount = r.price * row.quantity;
                    });
                    frm.refresh_field('products');
                   
                }
            }
        }, 1000)

 
    }
});