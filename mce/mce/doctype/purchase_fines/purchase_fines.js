// Copyright (c) 2025, MCE and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Fines", {
	refresh: function(frm) {
        set_autocompletions_for_condition_formula(frm);
	},
    onload : function(frm){
        set_autocompletions_for_condition_formula(frm);
    },
    formula_based_criteria : function(frm) {
        set_autocompletions_for_condition_formula(frm);
        if (frm.doc.formula_based_criteria == 0 ){
            frm.doc.value =0;
            
        }
    }
});

function set_autocompletions_for_condition_formula(frm) {
    const autocompletions = [];
    frappe.run_serially([
        () => {
            return frappe.model.with_doctype("Purchase Receipt", () => {
                const po_fields = frappe.get_meta("Purchase Receipt").fields;
                autocompletions.push(
                    ...po_fields.map((f) => ({
                        value: f.fieldname,
                        score: 10,
                        meta: __("Purchase Receipt Field"),
                    }))
                );
            });
        },
        () => {
        
            ["fines_formula"].forEach((field) => {
                frm.set_df_property(field, "autocompletions", autocompletions);
            });
            frm.refresh_field("fines_formula");
        },
    ]);
    
}