frappe.ui.form.on('Terms Details', {
    terms_and_conditions: function(frm , cdt ,cdn){
        let row = locals[cdt][cdn];
        if (row.terms_and_conditions){ 
            frappe.call({
                method:'mce.custom.blanket_order.blanket_order.get_terms_details', 
                args:{
                    term : row.terms_and_conditions
                }, 
                callback: function(r){
                    frappe.model.set_value(cdt, cdn, "editor", r.message);
                    frm.refresh_field("custom_term");
                }
            })
        } else { 
            frappe.model.set_value(cdt, cdn, "editor", null);
            frm.refresh_field("custom_term");
        }
    },
});
//
frappe.ui.form.on('Blanket Order', {
    refresh: function(frm){
        filter_items(frm);
    },
    supplier: function(frm) {
        filter_items(frm);
    }
});



function filter_items(frm) {
    if (frm.doc.blanket_order_type === 'Purchasing' && frm.doc.supplier){ 
        frappe.call({
            method:'mce.custom.blanket_order.blanket_order.get_party_items', 
            args:{
                supp : frm.doc.supplier
            }, 
            callback: function(r){
                if (r.message){
                    console.log("Success");
                    console.log(r.message);
                    const items_list = r.message
                    frm.fields_dict["items"].grid.get_field("item_code").get_query = function(doc) {
                        return {
                            filters: {
                                "item_code": ["in", items_list]
                            }
                        }
                    }
                    frm.refresh_field("items");
                }
            }
        })
    }
}