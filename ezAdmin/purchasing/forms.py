from django import forms
from .models import *
import requests
#from mixins.validation_mixin import QuantityValidationMixin
from django.core.exceptions import ValidationError
from django.db.models import F, Sum, Value
from collections import OrderedDict

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'address', 'representative_name', 'phone_number', 'email', 'currency_trade']

class PurchasingDocumentForm(forms.ModelForm):
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc', 'k1_form_rate', 'AWB_number', 'AWB_doc']
        
    def __init__(self, *args, **kwargs):
        super(PurchasingDocumentForm, self).__init__(*args, **kwargs)
        self.fields['po_doc'].widget.attrs['class'] = 'form-control-file'