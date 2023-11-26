from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError
from mixins.file_size_mixin import FileValidatorMixin

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

class ElectronicPurchasingDocumentForm(FileValidatorMixin, forms.ModelForm):
    allowed_extensions = ['pdf']
    class Meta:
        model = ElectronicPurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc']
    
    def clean(self):
        cleaned_data = super().clean()
        po_doc = cleaned_data.get('po_doc')
        invoice_doc = cleaned_data.get('invoice_doc')
        
        self.validate_file_size(po_doc, 'po_doc')
        self.validate_file_size(invoice_doc, 'invoice_doc')

        self.validate_file_extension(po_doc, 'po_doc')
        self.validate_file_extension(invoice_doc, 'invoice_doc')

        return cleaned_data

class ElectronicInventoryForm(forms.ModelForm):
    class Meta:
        model = ElectronicInventory
        fields = ['electronic_item', 'serial_number', 
            'price_per_unit', 'purchasing_document', 
            'date_of_purchase', 'status', 'remark']
        widgets = {
            'date_of_purchase': forms.DateInput(attrs={'type': 'date'})
        }
    
class ElectronicTransactionForm(FileValidatorMixin, forms.ModelForm):
    allowed_extensions = ['pdf', 'png', 'jpeg']
    class Meta:
        model = ElectronicTransaction
        fields = ['current_user', 'electronic_item', 
            'transaction_type', 'initial_agreement_doc', 
            'return_agreement_doc']
    
    def get_idle_items(self):
        return ElectronicInventory.objects.filter(status='Idle')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the queryset for the electronic_item field to include only items with status 'Idle'
        self.fields['electronic_item'].queryset = self.get_idle_items()

        # If the instance exists (when updating the form) and has a value for electronic_item, include it in the queryset
        if self.instance and self.instance.transaction_type == 'Checked-Out' and hasattr(self.instance, 'electronic_item') and self.instance.electronic_item:
            self.fields['electronic_item'].queryset |= ElectronicInventory.objects.filter(pk=self.instance.electronic_item.pk)
        elif not self.instance:
            # For create form, set the initial queryset to include only 'Idle' items
            self.fields['electronic_item'].queryset = self.get_idle_items()

        if not self.get_idle_items().exists():
            self.fields['electronic_item'].empty_label = "No electronic items available"
        else:
            self.fields['electronic_item'].empty_label = "Select an electronic item"

    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        initial_agreement_doc = cleaned_data.get('initial_agreement_doc')
        return_agreement_doc = cleaned_data.get('return_agreement_doc')

        if transaction_type == 'Checked-In':
            # Validate return_agreement_doc for Checked-In transactions
            if not return_agreement_doc:
                self.add_error("return_agreement_doc", "Return agreement document is required for Checked-In transactions.")
            else:
                # Validate file size only when it's a Checked-In transaction
                self.validate_file_size(return_agreement_doc, 'return_agreement_doc')
                # Validate file extension for Checked-In transactions
                self.validate_file_extension(return_agreement_doc, 'return_agreement_doc')

        # Validate file size for both transaction types
        self.validate_file_size(initial_agreement_doc, 'initial_agreement_doc')

        # Validate file extension for both transaction types
        self.validate_file_extension(initial_agreement_doc, 'initial_agreement_doc')
        

        return cleaned_data
