import frappe 


def validate(self , method):
    recheck_terms_checks(self)
    accounts_table_validation(self)
    
    
def recheck_terms_checks(self):
    if self.buying == 0 : 
        self.custom_blanket_order_term = 0
        self.custom_has_accounting_effect = 0
    if self.buying and self.custom_blanket_order_term == 0 : 
        self.custom_has_accounting_effect = 0 
    if self.custom_has_accounting_effect ==  0:
        self.custom_accounts = list()
        
def accounts_table_validation(self):  
    if self.custom_has_accounting_effect: 
        debit_count, credit_count = 0, 0
        for r in self.custom_accounts:
            if (r.formula_based_criteria == 0 and r.value == 0) or ( r.formula_based_criteria == 1 and r.condition_formula is None ) :
                frappe.throw(f'Row {r.idx}: Set Value or Condition Formula.')
            if r.transaction_type == 'Debit':
                debit_count += 1
            elif r.transaction_type == 'Credit':
                credit_count += 1
        if debit_count == 0 or credit_count == 0:
            frappe.throw(
                "At least one debit and one credit entry are required in the accounts."
            )