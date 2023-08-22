frappe.listview_settings['Quotation'] = {
    get_indicator(doc) {
        if (doc.docstatus == 1) {

            return [__("Confirmed"), "green"];
        }
        else {
            return [__("Draft"), "green"];
        }

    }
}

