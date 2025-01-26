frappe.ui.form.on('Purchase Receipt', {
    setup: function(frm) {
        Filter(frm);
    },
    refresh: function(frm) {
        Filter(frm);
    },
    onload: function(frm) {
        Filter(frm);
    },
});

frappe.ui.form.on('Fines Details', {
    form_render: function(frm) {
        Filter(frm);
    },
});

function Filter(frm) {
    frappe.call({
        method: "mce.custom.purchase_receipt.purchase_receipt.get_fines_names",
        args: {
            self: frm.doc
        },
        callback: function(r) {
            if (r.message) {
                const finesList = r.message;
                console.log(finesList);
                frm.fields_dict["custom_fines"].grid.get_field("purchase_fines").get_query = function(doc) {
                    return {
                        filters: {
                            "fines_name": ["in", finesList]
                        }
                    }
                }
            }
            
        }
    });
}