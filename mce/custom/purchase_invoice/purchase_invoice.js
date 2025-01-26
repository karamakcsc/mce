frappe.ui.form.on('Purchase Invoice Item', {
    items_add: function(frm , cdt , cdn){
        GetFines(frm);
    }, 
    items_remove: function(frm , cdt , cdn){
        GetFines(frm);
    }
});
frappe.ui.form.on('Purchase Invoice',{
    total: function(frm){
        GetFines(frm);
    }
});


function GetFines(frm){
    frappe.call({
        method :"mce.custom.purchase_invoice.purchase_invoice.get_fines_whitelist", 
        args:{
            self : frm.doc
        },
        callback: function(r){
            frm.refresh_field("Custom_fines");
            frm.refresh_field("custom_total_fines");
        }
       })
}