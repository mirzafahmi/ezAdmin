from django import forms
from dashboard.models import *
from django.forms import inlineformset_factory

class CustomerQuotationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'posscode','pic_name', 'email', 'phone_number', 'sales_person', 'currency']

class QuotationForm(forms.ModelForm):
    
    class Meta:
        model = Quotation
        fields = ['customer_id', 'doc_number']

    def save(self, commit=True):
        quotation = super().save(commit=False)
        if not quotation.doc_number:
            # Generate doc_number
            quotation.doc_number = f'QT/{quotation.customer_id.sales_person.name_acronym}/{quotation.customer_id.name_acronym}/{timezone.localtime(timezone.now()).strftime("%Y%m%d")}'

        if commit:
            quotation.save()
            
        return quotation

    def __init__(self, *args, **kwargs):
        disable_customer_id = kwargs.pop('disable_customer_id', False)
        super().__init__(*args, **kwargs)

        if disable_customer_id:
            self.fields['customer_id'].widget.attrs['disabled'] = 'disabled'

        # Disable the doc_number field
        self.fields['doc_number'].widget.attrs['disabled'] = 'disabled'

        self.fields['doc_number'].widget.attrs['placeholder'] = 'Auto-generated'
        

class QuotationItemForm(forms.ModelForm):
    class Meta:
            model = QuotationItem
            fields = ['quotation', 'product', 'quantity', 'price', 'id']
    
    def __init__(self, *args, **kwargs):
        quotation_instance = kwargs.pop('quotation_instance', None)
        super(QuotationItemForm, self).__init__(*args, **kwargs)

        # Set the initial value for the 'quotation' field
        if quotation_instance:
            self.fields['quotation'].initial = quotation_instance.id
            self.fields['quotation'].widget = forms.HiddenInput()

class OrderExecutionForm(forms.ModelForm):
    class Meta:
        model = OrderExecution
        fields = ['quotation_id', 'delivery_method', 'tracking_number']

