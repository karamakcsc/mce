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
    }
    
});
