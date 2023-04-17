frappe.listview_settings['Customer Invoice'] = {
    add_fields: ['total_remaining_quantity'],
    hide_name_column: false, // hide the last column which shows the `name`
    // set this to true to apply indicator function on draft documents too
    has_indicator_for_draft: false,

    get_indicator(doc) {
        if(doc.docstatus==1){
            if(doc.total_remaining_quantity>0){ 
                return [__("Remaining"), "red"];
            } 
        
        }
    },
}
