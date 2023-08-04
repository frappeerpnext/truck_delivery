frappe.listview_settings['Request for Quotation'] = {
    add_fields: ['total_purchase_order'],
    hide_name_column: false, // hide the last column which shows the `name`
    // set this to true to apply indicator function on draft documents too
    has_indicator_for_draft: false,

    get_indicator(doc) {
        if(doc.docstatus==1){
          
            if(doc.total_purchase_order>0){
                alert(1)
                return [__("Purchase Order"), "red"];
            } 
            else{ 
                return [__("RFQ"), "green"];
            } 
        
        }
    },
}
