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
        fields = ['company_name', 'address', 'representative_name', 'phone_number', 'email', 'currency_trade']

class PurchasingDocumentForm(FileValidatorMixin, forms.ModelForm):
    allowed_extensions = ['pdf']
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 
            'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc', 
            'k1_form_rate', 'AWB_number', 'AWB_doc']
        
    def __init__(self, *args, **kwargs):
        super(PurchasingDocumentForm, self).__init__(*args, **kwargs)
        self.fields['po_doc'].widget.attrs['class'] = 'form-control-file'
        
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
