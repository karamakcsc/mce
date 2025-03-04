import frappe



@frappe.whitelist()
def get_terms_details(term):
    style = """
            <style>
                .wide-table { width: 100%; }
                .first-column { width: 40%;}
                .text-left {text-align: left;  width: 30%;}
            </style>
        """
    html = """  <div class="container mt-3">"""
    html+= """      <table class="table table-bordered table-hover wide-table">"""
    html+= """          <thead class="thead-light"> """
    html+= """              <tr> """
    html+= """                  <th scope="col" class="first-column">Account</th>"""
    html+= """                  <th scope="col" class="text-left">Debit</th>"""
    html+= """                  <th scope="col" class="text-left">Credit</th> """
    html+= """              </tr> """ 
    html+= """          </thead> """
    html += "           <tbody>"
    term_doc = frappe.get_doc('Terms and Conditions' , term)
    if term_doc.custom_has_accounting_effect: 
        for r in term_doc.custom_accounts: 
            html += "           <tr>"
            html += f"              <td>{r.account}</td>"
            if r.transaction_type == "Debit": 
                if r.formula_based_criteria:
                    html += f"              <td>{r.condition_formula}</td>"
                else: 
                    html += f"              <td>{r.value}</td>"
                html += f"              <td>0</td>" 
            
            elif r.transaction_type == "Credit": 
                html += f"              <td>0</td>" 
                if r.formula_based_criteria:
                    html += f"              <td>{r.condition_formula}</td>"
                else: 
                    html += f"              <td>{r.value}</td>"
        return style+html
        
@frappe.whitelist()
def get_party_items(supp):
    items_list = frappe.db.sql("""
                SELECT based_on_value 
                FROM `tabParty Specific Item` 
                WHERE party_type = 'Supplier' 
                    AND party = %s 
                    AND restrict_based_on = 'Item'
            """,(supp,), as_dict=True)
    
    return [item['based_on_value'] for item in items_list]