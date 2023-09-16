from django import forms
from dashboard.models import *
from django.forms import inlineformset_factory

class CustomerQuotationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'posscode','pic_name', 'email', 'phone_number', 'sales_person', 'currency']

class QuotationForm(forms.ModelForm):
    #customer_id = forms.ModelChoiceField(queryset = Customer.objects.all(),required = True) 
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

class QuotationItemForm(forms.ModelForm):
    class Meta:
            model = QuotationItem
            fields = ['product', 'quantity', 'price']

class QuotationItemForm2(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = ['product', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['customer_id'] = forms.ModelChoiceField(
            queryset = Customer.objects.all(),
            required=False,
            empty_label='Select an existing csutomer',
            widget=forms.Select(attrs={'class': 'form-control'}),
        )

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_id')
        
        try:
            customer = Quotation.objects.get(customer_id = customer_name)
        except Quotation.DoesNotExist:
            customer = Quotation.objects.create(customer_id = customer_name)

        # Update the author field in the form
        self.instance.quotation = customer

        return cleaned_data