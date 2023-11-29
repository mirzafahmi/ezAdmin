from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError
from django.db.models import F, Sum, Value
from collections import OrderedDict
from mixins.file_size_mixin import FileValidatorMixin

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'address', 'representative_name', 
        'phone_number', 'email', 'currency_trade']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['company_name'].widget.attrs['placeholder'] = 'Enter supplier company name'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter supplier address'
        self.fields['representative_name'].widget.attrs['placeholder'] = 'Enter supplier PIC name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter supplier phone number'
        self.fields['email'].widget.attrs['placeholder'] = f"Enter supplier PIC's email"

        self.fields['currency_trade'].empty_label = "Select a currency trade code"

        self.fields['phone_number'].initial = '+60'

class PurchasingDocumentForm(FileValidatorMixin, forms.ModelForm):
    allowed_extensions = ['pdf']
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 
            'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc', 
            'k1_form_rate', 'AWB_number', 'AWB_doc']
        
    def __init__(self, *args, **kwargs):
        super(PurchasingDocumentForm, self).__init__(*args, **kwargs)
        
        self.fields['po_number'].widget.attrs['placeholder'] = f"Enter a PO number"
        self.fields['invoice_number'].widget.attrs['placeholder'] = f"Enter a Invoice number"
        self.fields['packing_list'].widget.attrs['placeholder'] = f"Enter a Packing List number"
        self.fields['k1_form'].widget.attrs['placeholder'] = f"Enter a K1 Form number"
        self.fields['k1_form_rate'].widget.attrs['placeholder'] = f"Enter a K1 Form Rate"
        self.fields['AWB_number'].widget.attrs['placeholder'] = f"Enter a AWB number"

        self.fields['supplier'].empty_label = "Select a supplier"
        
    def clean(self):
        cleaned_data = super().clean()
        po_doc = cleaned_data.get('po_doc')
        invoice_doc = cleaned_data.get('invoice_doc')
        pl_doc = cleaned_data.get('pl_doc')
        k1_doc = cleaned_data.get('k1_doc')
        AWB_doc = cleaned_data.get('AWB_doc')

        self.validate_file_size(po_doc, 'po_doc')
        self.validate_file_size(invoice_doc, 'invoice_doc')
        self.validate_file_size(pl_doc, 'pl_doc')
        self.validate_file_size(k1_doc, 'k1_doc')
        self.validate_file_size(AWB_doc, 'AWB_doc')

        self.validate_file_extension(po_doc, 'po_doc')
        self.validate_file_extension(invoice_doc, 'invoice_doc')
        self.validate_file_extension(pl_doc, 'pl_doc')
        self.validate_file_extension(k1_doc, 'k1_doc')
        self.validate_file_extension(AWB_doc, 'AWB_doc')

        return cleaned_data
