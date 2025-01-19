frappe.ui.form.on("Condition and Infraction Details", {
    form_render: function (frm, cdt, cdn) {
        const child_row = locals[cdt][cdn];
        set_autocompletions_for_condition_formula(frm, cdt, cdn, child_row);
    },
    formula_based_criteria : function (frm, cdt, cdn) {
        const child_row = locals[cdt][cdn];
        set_autocompletions_for_condition_formula(frm, cdt, cdn, child_row);
    },
    onload_post_render: function (frm, cdt, cdn) {
        const child_row = locals[cdt][cdn];
        set_autocompletions_for_condition_formula(frm, cdt, cdn, child_row);
    },
    custom_accounts_add:function (frm, cdt, cdn) {
        const child_row = locals[cdt][cdn];
        set_autocompletions_for_condition_formula(frm, cdt, cdn, child_row);
    }
});

function set_autocompletions_for_condition_formula(frm, cdt, cdn, child_row) {
    const autocompletions = [];
    frappe.run_serially([
        () => {
            return frappe.model.with_doctype("Purchase Order", () => {
                const po_fields = frappe.get_meta("Purchase Order").fields;
                autocompletions.push(
                    ...po_fields.map((f) => ({
                        value: f.fieldname,
                        score: 10,
                        meta: __("Purchase Order Field"),
                    }))
                );
            });
        },
        () => {
            ["condition_formula"].forEach((field) => {
                frm.set_df_property(
                    child_row.parentfield,
                    "autocompletions",
                    autocompletions,
                    frm.doc.name,
                    field,
                    child_row.name
                );
            });
            console.log(frm.set_df_property(
                child_row.parentfield,
                "autocompletions",
                autocompletions,
                frm.doc.name,
                field,
                child_row.name
            ));
            frm.refresh_field(child_row.parentfield);
            console.log(child_row.parentfield);
        },
    ]);
    
}