frappe.listview_settings['Transportation Payment'] = {
    get_indicator(doc) {
        if (doc.docstatus == 1) {

            return [__("Confirmed"), "green"];
        }
        else {
            return [__("Draft"), "green"];
        }

    }
}

