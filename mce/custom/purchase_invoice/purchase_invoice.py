import frappe 
import json 
from mce.custom.purchase_order.purchase_order import formula_to_value
from erpnext.accounts.general_ledger import make_gl_entries
def validate(self , method): 
    get_fines(self)
    
def on_submit(self , method):
    make_gl(self)
    
def get_supplier_account(self):
    supplier_doc = frappe.get_doc('Supplier' , self.supplier)
    account = None
    for acc in  supplier_doc.accounts:
        if acc.company == self.company: 
            account = acc.account
    if account is not None: 
        return account
    if supplier_doc.supplier_group is not None: 
        group_doc = frappe.get_doc('Supplier Group', supplier_doc.supplier_group)
        for acc_g in group_doc.accounts: 
            if acc_g.company == self.company:
                account  = acc_g.account
    if account is not None: 
        return account
    company_doc = frappe.get_doc('Company' , self.company)
    if company_doc.default_receivable_account:
        return company_doc.default_receivable_account
    return None
def get_cost_center(self): 
    company_doc = frappe.get_doc('Company' , self.company)
    return company_doc.cost_center
        
    
@frappe.whitelist()
def get_fines_whitelist(self): 
    self = frappe._dict(json.loads(self))
    return get_fines(self)
    
def get_fines(self): 
    pr_list = list()
    for i in self.get('items'):
        if isinstance(i, dict) and i.get('purchase_receipt'):
            pr_list.append(i.get('purchase_receipt'))
        elif hasattr(i, 'purchase_receipt'):
            pr_list.append(i.purchase_receipt)
    pr_list = list(set(pr_list))
    self.custom_fines  , total_fines = list() , 0 
    if len(pr_list) != 0 : 
        for pr in pr_list:
            pr_doc = frappe.get_doc('Purchase Receipt' , pr)
            if len(pr_doc.custom_fines) !=0: 
                for fines in pr_doc.custom_fines: 
                    if fines.has_accounting_effect:
                        if fines.formula_based_criteria:
                            
                            amount = formula_to_value(pr_doc, fines.fines_formula)
                        else: 
                            amount = fines.amount
                        self.append('custom_fines', {
                           'purchase_fines' : fines.purchase_fines,
                           'purchase_receipt' : pr,
                           'revenue_acount': fines.account, 
                           'amount': amount     
                        })
                        total_fines += amount
    self.custom_total_fines = total_fines           
    return True
            
def make_gl(self): 
    if len(self.custom_fines) != 0 :
        gl_entries = list() 
        supplier_account = get_supplier_account(self)
        if supplier_account is None: 
            frappe.throw('Set Account in Supplier or Supplier Group or Company.')
        for r in self.custom_fines: 
            gl_entries.append(
                        self.get_gl_dict({
                        "account": r.revenue_acount,
                        "against": supplier_account,
                        "cost_center" : get_cost_center(self),
                        "credit_in_account_currency": r.amount,
                        "credit": r.amount,
                        "remarks": f"Fines:{r.purchase_fines} from Purchase Receipt : {r.purchase_receipt}"
                        }))
            gl_entries.append(
                        self.get_gl_dict({
                        "account": supplier_account,
                        "against":  r.revenue_acount,
                        "cost_center" : get_cost_center(self),
                        "debit_in_account_currency": r.amount,
                        "debit": r.amount,
                        "party_type" : 'Supplier', 
                        "party" : self.supplier,
                        "remarks": f"Fines:{r.purchase_fines} from Purchase Receipt : {r.purchase_receipt}"
                        }))
        if gl_entries: 
            make_gl_entries(gl_entries, cancel=0, adv_adj=0)