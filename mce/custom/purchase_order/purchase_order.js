
frappe.ui.form.on('Purchase Order', {
    refresh: function (frm) {
        hide_buttons(frm);
        CreditAndDebitTotals(frm);
    },
    onload: function(frm) {
        hide_buttons(frm);
        CreditAndDebitTotals(frm);
    },
    setup: function(frm) {
        hide_buttons(frm);
        CreditAndDebitTotals(frm);
    }, 
    grand_total: function(frm){
        CreditAndDebitTotals(frm);
    }
});

function hide_buttons(frm) {
    if (frappe.session.user !== 'Administrator') {
        setTimeout(() => {
            frm.page.wrapper.find('.inner-group-button:contains("Tools")').hide();
            frm.page.wrapper.find('.inner-group-button:contains("Get Items From")').hide();
        }, 5);
    }
}



function CreditAndDebitTotals(frm){
    if (frm.doc.docstatus === 0){
        frappe.call({
            method: "mce.custom.purchase_order.purchase_order.debit_and_credit_totals_whitelist",
            args: {
                self: frm.doc
            },
            callback:function(r) { 
                console.log(r.message);
                frappe.model.set_value(frm.doctype, frm.docname, 'custom_total_debit',  r.message.total_debit);
                frappe.model.set_value(frm.doctype, frm.docname, 'custom_total_credit',  r.message.total_credit);
                frm.refresh_field("custom_total_debit");
                frm.refresh_field("custom_total_credit");
            }
        });
    }
}
frappe.ui.form.on('Purchase Order', {
    setup(frm) {
        frm.fields_dict['custom_blanket_order'].get_query = function(doc) {
            return {
                filters: [
                    ["Blanket Order", "docstatus", "=", 1], 
                    ["Blanket Order", "supplier", "=", doc.supplier],
                    ["Blanket Order", "company", "=", doc.company]
                ]
            };
        };
    }, 
    custom_blanket_order: function(frm) { 
        if(frm.doc.custom_blanket_order){
            GetTremsData(frm);
        }
    }
});

function GetTremsData(frm){
    frappe.call({
        method: 'mce.custom.purchase_order.purchase_order.get_blanket_order_terms', 
        args: {
            bo_name : frm.doc.custom_blanket_order
        },
        callback: function(r){
            frm.clear_table("custom_term");
            r.message.forEach(function(row) {
                let child = frm.add_child("custom_term");
                // Set values for each child row
                frappe.model.set_value(child.doctype, child.name, "terms_and_conditions", row.terms_and_conditions);
                frappe.model.set_value(child.doctype, child.name, "has_accounting_effect", row.has_accounting_effect);
                frappe.model.set_value(child.doctype, child.name, "editor", row.editor);
                
            });
            frm.refresh_field("custom_term");
            CreditAndDebitTotals(frm);
        } 
    })
}

frappe.ui.form.on('Purchase Order', {
    custom_blanket_order(frm) {
        if (frm.doc.custom_blanket_order) {
            frm.add_custom_button(__('Add Items from Blanket Order'), function() {
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'Blanket Order',
                        name: frm.doc.custom_blanket_order
                    },
                    callback: function(r) {
                        if (r.message) {
                            let blanket_order_items = r.message.items;

                            let dialog = new frappe.ui.Dialog({
                                title: __('Select Items to Add'),
                                fields: [
                                    {
                                        fieldtype: 'Table',
                                        fieldname: 'items',
                                        label: __('Items'),
                                        fields: [
                                            { fieldtype: 'Data', fieldname: 'item_code', label: __('Item Code'), read_only: 1, in_list_view: 1 },
                                            { fieldtype: 'Float', fieldname: 'qty', label: __('Quantity'), in_list_view: 1 },
                                            { fieldtype: 'Currency', fieldname: 'rate', label: __('Rate'), in_list_view: 1 },
                                            { fieldtype: 'Float', fieldname: 'ordered_qty', label: __('Ordered Qty'), in_list_view: 0 }
                                        ],
                                        data: blanket_order_items.map(item => ({
                                            item_code: item.item_code,
                                            qty: item.qty - (item.ordered_qty || 0),
                                            rate: item.rate,
                                            ordered_qty: item.ordered_qty || 0
                                        }))
                                    }
                                ],
                                primary_action: function() {
                                    let values = dialog.get_values();
                                    frm.clear_table("items");
                                    if (values && values.items) {
                                        
                                        values.items.forEach(function(item) {
                                            
                                            if (item.__checked) {
                                                let child = frm.add_child("items");
                                                // Set values for each child row
                                                frappe.model.set_value(child.doctype, child.name, "item_code",item.item_code)
                                                .then(() =>frappe.model.set_value(child.doctype, child.name, "qty", item.qty))
                                                .then(() =>frappe.model.set_value(child.doctype, child.name, "rate", item.rate))
                                                .then(() =>frappe.model.set_value(child.doctype, child.name, "against_blanket_order",1))
                                                .then(() =>frappe.model.set_value(child.doctype, child.name, "blanket_order",frm.doc.custom_blanket_order))
                                                .then(() => resolve());
                    
                                            }
                                        });
                                        frm.refresh_field('items');
                                    }
                                    dialog.hide();
                                },
                                primary_action_label: __('Add Selected Items')
                            });
                            dialog.show();
                        }
                    }
                });
            });
        }
    }
});