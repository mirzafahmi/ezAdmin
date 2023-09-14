from django import forms
from dashboard.models import *

class CustomerQuotationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'posscode','pic_name', 'email', 'phone_number', 'sales_person', 'currency']

class QuotationForm(forms.ModelForm):
    customer_id = forms.ModelChoiceField(queryset = Customer.objects.all(),required = True) 
    class Meta:
        model = Quotation
        fields = ['customer_id', 'doc_number']

class QuotationItemForm(forms.ModelForm):
    class Meta:
            model = QuotationItem
            fields = ['quotation', 'product', 'quantity', 'price']