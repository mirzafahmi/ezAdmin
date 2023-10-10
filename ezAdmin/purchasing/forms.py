from django import forms
from .models import *

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'address', 'representative_name', 'phone_number', 'email']

class PurchasingDocumentForm(forms.ModelForm):
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc']
        
class RawMaterialIdentifierForm(forms.ModelForm):
    class Meta:
        model = RawMaterialIdentifier
        fields = ['parent_item_code']

class RawMaterialComponentForm(forms.ModelForm):
    class Meta:
        model = RawMaterialComponent
        fields = ['component', 'spec', 'identifier']

class BOMComponentForm(forms.ModelForm):
    class Meta:
        model = BOMComponent
        fields = ['product', 'raw_material_component', 'quantity_used']