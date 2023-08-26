// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Invoice', {
    refresh: function (frm) {
        if(!frm.doc.__islocal){
            const d = frm.doc;
            frm.dashboard.add_indicator(__("Total Quantity: {0}",[d.total_quantity]) ,"blue");
            frm.dashboard.add_indicator(__("Total Amount: {0}",[format_currency(frm.doc.total_amount)]) ,"blue");
            frm.dashboard.add_indicator(__("Paid: {0}",[format_currency(frm.doc.total_paid)]) ,"green");
            frm.dashboard.add_indicator(__("Balance: {0}",[format_currency(frm.doc.balance)]) ,"red");
        
        }
        frm.set_query('quotation', function() {
            return {
                'filters': {
                    "docstatus": 1
                }
            };
        });	
			 
			
		 
    },
    onload: function (frm) {
        setTimeout(function () {
           
            if (frm.doc.purchase_order) {
             
             
                if (frm.doc.__islocal) {
                   
                    const data = frappe.get_doc("Purchase Order", frm.doc.purchase_order)
                    
                    data.products.forEach(r => {
                        if(r.remaining_quantity>0){
                            var row = frappe.model.add_child(frm.doc, '', 'products');
                            row.purchase_order_product_id = r.name;
                            row.product_code = r.product_code;
                            row.product_name = r.product_name;
                            row.unit = r.unit;
                            row.quantity = r.remaining_quantity ;
                            row.price = r.price;
                            row.total_amount = r.price * r.remaining_quantity;
                            row.purchase_quantity = r.quantity;
                        }
                    });
                   
                    frm.refresh_field('products');
                    frm.doc.district = frm.doc.customer_district;
                    frm.refresh_field('district');
                    
                   
                }
            }
        }, 1000)

 
    }
});


frappe.ui.form.on('Customer Invoice Product', {
    price:function (frm,cdt, cdn) {
     let doc = locals[cdt][cdn];
     UpdateProductAmount(frm,doc)
   }, 
   quantity:function (frm,cdt, cdn) {
     UpdateProductAmount(frm,locals[cdt][cdn])
   }, 

 })
 

function UpdateProductAmount(frm,doc){
        doc.total_amount  =( doc.quantity ||  0 ) * (doc.price || 0 );
        refresh_field('products');
        
    
}
