// Copyright (c) 2023, tes pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quotation", {
    refresh(frm) {
        if (!frm.doc.__islocal) {
            const d = frm.doc;
            frm.dashboard.add_indicator(__("Total Cost: {0}".toUpperCase(), [format_currency(d.total_cost)]), "blue");
            frm.dashboard.add_indicator(__("Total Selling: {0}".toUpperCase(), [format_currency(d.total_selling_price)]), "orange");
            if (d.total_selling_price > d.total_cost + d.total_additional_cost) {
                frm.dashboard.add_indicator(__("Prifit: {0}".toUpperCase(), [format_currency(d.profit)]), "green");
            } else {
                frm.dashboard.add_indicator(__("Loss: {0}".toUpperCase(), [format_currency(d.loss)]), "red");
            }

        }
        if (frm.is_new()) {
            let data = localStorage.getItem('quotation-param')
            data = JSON.parse(data)
            frm.set_value('customer', data.customer)
            frm.set_value('start_date', data.start)
            frm.set_value('end_date', data.end)
            frm.set_value('quotation_date', frappe.datetime.nowdate())
        }


    },
    after_save(frm) {
        if (localStorage.getItem('quotation-param')) {
            localStorage.removeItem('quotation-param')
        }
    }

});
frappe.ui.form.on('Customer Quotation Product', {
    quantity: function (frm, cdt, cdn) {
        calculate_cost(frm, cdt, cdn)
        calculate_mark_up_amount(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        calculate_markup_percent(frm, cdt, cdn)
        frm.refresh_field("product");
    },
    cost: function (frm, cdt, cdn) {
        calculate_cost(frm, cdt, cdn);
        calculate_mark_up_amount(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        calculate_markup_percent(frm, cdt, cdn)
        frm.refresh_field("product");

    },
    original_cost: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        child.cost=child.original_cost - child.rebate;
        var total_cost = (child.cost + child.additional_cost + child.additional_cost_2 + child.additional_cost_3) * child.quantity;
        child.total_cost=total_cost;
        let selling_price = child.total_cost + child.markup_amount;
        child.selling_price=selling_price;
        let markup_percent = (child.markup_amount * 100) / child.total_cost
        child.markup_percent=markup_percent;
        child.total_additional_cost=child.additional_cost + child.additional_cost_2 + child.additional_cost_3;
        calculate_selling_price(frm, cdt, cdn)
        frm.refresh_field("product");
    },
    additional_cost: function (frm, cdt, cdn) {
        calculate_cost(frm, cdt, cdn);
        calculate_mark_up_amount(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        calculate_markup_percent(frm, cdt, cdn)
        frm.refresh_field("product");
    },
    additional_cost_2: function (frm, cdt, cdn) {
        calculate_cost(frm, cdt, cdn);
        calculate_mark_up_amount(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        calculate_markup_percent(frm, cdt, cdn)
        
        frm.refresh_field("product");
    },
    additional_cost_3: function (frm, cdt, cdn) {
        calculate_cost(frm, cdt, cdn);
        calculate_mark_up_amount(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        calculate_markup_percent(frm, cdt, cdn)
        frm.refresh_field("product");
    },

    markup_amount: function (frm, cdt, cdn) {
        calculate_markup_percent(frm, cdt, cdn)
        calculate_selling_price(frm, cdt, cdn)
        frm.refresh_field("product");
    },
    general_markup_amount:function(frm, cdt, cdn){
        var child = locals[cdt][cdn];
        child.general_markup_percent = (child.markup_amount * 100) / child.total_cost;
        child.general_price = child.total_cost + child.general_markup_amount;
        frm.refresh_field("product");
        
    },
    rebate: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var cost = (child.original_cost - child.rebate);
        child.cost=cost;
        frm.refresh_field("product");
    },

    qty_quotation: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var total_selling_cost = child.qty_quotation * child.total_cost;
        var total_selling_quotation_price = child.qty_quotation * child.selling_price;
        child.total_cost_quotation=total_selling_cost;
        child.total_selling_quotation_price=total_selling_quotation_price;
        frm.refresh_field("product");
    },
    total_cost_quotation: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var total_selling_cost = child.qty_quotation * child.total_cost;
        var total_selling_quotation_price = child.qty_quotation * child.selling_price;
        child.total_cost_quotation=total_selling_cost;
        child.total_selling_quotation_price=total_selling_quotation_price;
        frm.refresh_field("product");
    },

});

function calculate_cost(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    var total_cost = (child.cost + child.additional_cost + child.additional_cost_2 + child.additional_cost_3) * child.quantity;
    child.cost = child.original_cost - child.rebate;
    var total_selling_cost = child.qty_quotation * child.total_cost;
    var total_selling_quotation_price = child.qty_quotation * child.selling_price;
    child.total_cost_quotation=total_selling_cost;
    child.total_selling_quotation_price = total_selling_quotation_price;
    child.total_cost=total_cost;
    child.total_additional_cost=(child.additional_cost + child.additional_cost_2 + child.additional_cost_3)
    frm.refresh_field("product");
}
function calculate_mark_up_amount(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    let markup_amount = child.total_cost * child.markup_percent / 100;
    var total_selling_cost = child.qty_quotation * child.total_cost;
    var total_selling_quotation_price = child.qty_quotation * child.selling_price;
    child.total_cost_quotation=total_selling_cost;
    child.total_selling_quotation_price=total_selling_quotation_price;
    child.markup_amount=markup_amount;
    frm.refresh_field("product");
}

function calculate_selling_price(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    let selling_price = child.total_cost + child.markup_amount;
    var total_selling_cost = child.qty_quotation * child.total_cost;
    var total_selling_quotation_price = child.qty_quotation * child.selling_price;
    child.total_cost_quotation=total_selling_cost;
    child.total_selling_quotation_price=total_selling_quotation_price;
    child.selling_price=selling_price;
    frm.refresh_field("product");
}
function calculate_markup_percent(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    let markup_percent = (child.markup_amount * 100) / child.total_cost;
    var total_selling_cost = child.qty_quotation * child.total_cost;
    var total_selling_quotation_price = child.qty_quotation * child.selling_price;
    child.total_cost_quotation=total_selling_cost;
    child.total_selling_quotation_price=total_selling_quotation_price;
    child.markup_percent=markup_percent;
    frm.refresh_field("product");
}