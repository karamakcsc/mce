import frappe
from frappe import _
import json
import unicodedata


@frappe.whitelist()
def get_blanket_order_terms(bo_name): 
    if bo_name: 
        bo_doc = frappe.get_doc('Blanket Order' , bo_name)
        return bo_doc.custom_term
    
    
@frappe.whitelist()
def debit_and_credit_totals_whitelist(self):
    self = frappe._dict(json.loads(self))
    total_debit , total_credit = debit_and_credit_totals(self)
    return {
        'total_debit' : total_debit, 
        'total_credit' : total_credit
    }

def validate(self, method):
    debit_and_credit_totals(self)
    
    
def on_submit(self , method): 
    accounting_validation(self)
    create_jv(self)

    
def debit_and_credit_totals(self): 
    total_credit, total_debit = 0, 0 
    for a in self.get('custom_term'):
        if isinstance(a, dict):
            term_doc = frappe.get_doc('Terms and Conditions' , a.get('terms_and_conditions'))
        else:
             term_doc = frappe.get_doc('Terms and Conditions' , a.terms_and_conditions)
        
        for t in term_doc.custom_accounts:
            if t.formula_based_criteria:
                amount = formula_to_value(self, t.condition_formula)
            else: 
                amount = t.value

            if t.transaction_type == "Debit":
                total_debit += amount
            elif t.transaction_type == "Credit":
                total_credit += amount
    self.custom_total_debit = total_debit
    self.custom_total_credit = total_credit
    return total_debit, total_credit


def formula_to_value(self ,condition_formula ):
    code = unicodedata.normalize("NFKC", condition_formula)
    whitelisted_globals = {"int": int, "float": float, "round": round}
    eval_globals = {"__builtins__": {}}
    eval_globals.update(whitelisted_globals)
    if isinstance(self, dict):
        eval_locals = self
    else:
        eval_locals = self.as_dict()
    return eval(code, eval_globals, eval_locals)


def accounting_validation(self): 
    if (self.custom_total_debit == 0) and  (self.custom_total_credit ==0):
        return True  
    if (self.custom_total_debit != 0) or (self.custom_total_credit !=0):
        if self.custom_total_debit != self.custom_total_credit : 
            frappe.throw('Total Debit and Total Credit must be equal.')
               
            
def create_jv(self):
    if len(self.custom_term) != 0 : 
        for term in self.custom_term:
            if term.terms_and_conditions: 
                jv = frappe.new_doc('Journal Entry')
                jv.posting_date = self.transaction_date
                jv.company = self.company
                jv.user_remark = f'Purchase Order: {self.name} For Term : {term.terms_and_conditions}'
                term_doc = frappe.get_doc('Terms and Conditions' , term.terms_and_conditions)
                if len(term_doc.custom_accounts) !=0:
                    for a in term_doc.custom_accounts: 
                        row = dict()
                        if a.formula_based_criteria: 
                            amount = formula_to_value(self, a.condition_formula)
                        else: 
                            amount = a.value
                        row['account'] = a.account
                        if a.transaction_type == "Debit":
                            row["debit_in_account_currency"] = amount
                            row["debit"] = amount
                        elif a.transaction_type == "Credit":
                            row["credit_in_account_currency"] = amount
                            row["credit"] = amount
                        account_doc = frappe.get_doc('Account', a.account)
                        if account_doc.account_type in ['Payable', 'Receivable', 'Liability', None]: 
                            row["party_type"] = 'Supplier'
                            row['party'] = self.supplier
                        jv.append("accounts", row)
                jv.insert(ignore_permissions=True)
                jv.submit()
                for r in jv.accounts: 
                    frappe.db.set_value(r.doctype , r.name ,'reference_type' , self.doctype )
                    frappe.db.set_value(r.doctype , r.name ,'reference_name' , self.name )
        frappe.msgprint(
            f"Journal Entry {jv.name} Created Successfully.",
            alert=True,
            indicator='green'
        )
            