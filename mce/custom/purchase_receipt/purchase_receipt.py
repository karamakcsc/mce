
import frappe 
import json


@frappe.whitelist()
def get_fines_names(self): 
    self = frappe._dict(json.loads(self))
    bo_list = list()
    for i in self.get('items'):
        if i.get('purchase_order'): 
            po_doc = frappe.get_doc('Purchase Order' ,i.get('purchase_order') )
            if po_doc.custom_blanket_order: 
                bo_list.append(po_doc.custom_blanket_order)
    bo_list = list(set(bo_list))
    fines_list = list()
    for bo in bo_list:
        bo_doc = frappe.get_doc('Blanket Order' , bo)
        if len(bo_doc.custom_fines) != 0: 
            for f in bo_doc.custom_fines: 
                if f.purchase_fines not in fines_list: 
                    fines_list.append(f.purchase_fines)
    return fines_list
