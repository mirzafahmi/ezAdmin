from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError

class ElectronicUserLocationForm(forms.ModelForm):
    class Meta:
        model = ElectronicUserLocation
        fields = ['company_name', 'careholder_name', 'phone_number']

class ElectronicUserForm(forms.ModelForm):
    class Meta:
        model = ElectronicUser
        fields = ['name', 'position', 'location']

class ElectronicBrandForm(forms.ModelForm):
    class Meta:
        model = ElectronicBrand
        fields = ['brand_name']

class ElectronicModelForm(forms.ModelForm):
    class Meta:
        model = ElectronicModel
        fields = ['brand', 'model_name']

class ElectronicPurchasingDocumentForm(forms.ModelForm):
    class Meta:
        model = ElectronicPurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc']

class ElectronicInventoryForm(forms.ModelForm):
    class Meta:
        model = ElectronicInventory
        fields = ['electronic_item', 'serial_number', 
            'price_per_unit', 'purchasing_document', 
            'date_of_purchase', 'status', 'remark']
        widgets = {
            'date_of_purchase': forms.DateInput(attrs={'type': 'date'})
        }
    
class ElectronicTransactionForm(forms.ModelForm):
    class Meta:
        model = ElectronicTransaction
        fields = ['current_user', 'electronic_item', 
            'transaction_type', 'initial_agreement_doc', 
            'return_agreement_doc']
    
    def get_queryset(self):
        if self.instance is None:
            return ElectronicInventory.objects.filter(status='Idle')
        else:
            return ElectronicInventory.objects.filter(status='Idle') | ElectronicInventory.objects.filter(pk=self.instance.pk)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        queryset = ElectronicInventory.objects.filter(status='Idle')
        print(queryset)
        self.fields['electronic_item'].queryset = self.get_queryset()

        if not self.get_queryset().exists():
            self.fields['electronic_item'].empty_label = "No electronic items available"
        else:
            self.fields['electronic_item'].empty_label = "Select an electronic item"

    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        return_agreement_doc = cleaned_data.get('return_agreement_doc')

        if transaction_type == 'Log-In' and not return_agreement_doc:
            self.add_error("return_agreement_doc", "Return agreement document is required for Log-In transactions.")

        return cleaned_data