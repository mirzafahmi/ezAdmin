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

class OrderExecutionForm(forms.ModelForm):
    class Meta:
        model = OrderExecution
        fields = ['quotation_id', 'do_number', 'inv_number', 'delivery_method', 'tracking_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(f"Form instance: {self.instance}")
        print(f"quotation_id: {self.instance.quotation_id}")
        print(f"Type of quotation_id: {type(self.instance.quotation_id)}")

        # Add fields for Quotation details
        self.fields['quotation_details'] = forms.CharField(
            widget=forms.Textarea(attrs={'readonly': 'readonly'}),
            required=False,
        )

        # Add fields for QuotationItem details
        self.fields['quotation_item_details'] = forms.CharField(
            widget=forms.Textarea(attrs={'readonly': 'readonly'}),
            required=False,
        )

        if self.instance.quotation_id:
            # Retrieve and populate Quotation details
            quotation = self.instance.quotation_id

            quotation_details = f"Quotation Details: {quotation.doc_number}"  # Replace with actual details
            self.initial['quotation_details'] = quotation_details

            # Retrieve and populate QuotationItem details
            quotation_items = QuotationItem.objects.filter(quotation=quotation.id)
            quotation_item_details = "\n".join([f"Item: {item.name}, Price: {item.price}" for item in quotation_items])
            self.initial['quotation_item_details'] = quotation_item_details

            print(quotation_details)
            print('1')
            print(quotation_item_details)
            print('2')
            print(self.fields['quotation_item_details'])