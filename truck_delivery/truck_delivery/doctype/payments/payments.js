// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payments", {
	refresh(frm) {

	},
    setup(frm) {
        frm.set_query("customer_invoice", function() {
            return {
                filters: [
                    ["Customer Invoice","docstatus", "=", 1]
                ]
            }
        });
    }
});
