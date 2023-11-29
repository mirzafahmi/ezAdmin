from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError
from mixins.file_size_mixin import FileValidatorMixin

class ElectronicUserLocationForm(forms.ModelForm):
    class Meta:
        model = ElectronicUserLocation
        fields = ['company_name', 'careholder_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['company_name'].widget.attrs['placeholder'] = 'Enter a Careholder Company Name'
        self.fields['careholder_name'].widget.attrs['placeholder'] = 'Enter a Careholder Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter a Careholder Phone Number'

        self.fields['phone_number'].initial = '+60'
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        cleaned_phone_number = ''.join(filter(str.isdigit, str(phone_number)))
        
        formatted_phone_number = f"+{cleaned_phone_number[0:2]} {cleaned_phone_number[2:4]}-{cleaned_phone_number[4:7]} {cleaned_phone_number[7:]}"

        return formatted_phone_number

class ElectronicUserForm(forms.ModelForm):
    class Meta:
        model = ElectronicUser
        fields = ['name', 'position', 'location']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Enter an User Name'
        self.fields['position'].widget.attrs['placeholder'] = 'Enter an User Position'
        
        self.fields['location'].empty_label = "Select an User Location"

class ElectronicBrandForm(forms.ModelForm):
    class Meta:
        model = ElectronicBrand
        fields = ['brand_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['brand_name'].widget.attrs['placeholder'] = 'Enter a Brand Name'

class ElectronicModelForm(forms.ModelForm):
    class Meta:
        model = ElectronicModel
        fields = ['brand', 'model_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['model_name'].widget.attrs['placeholder'] = 'Enter a Model Name'
        
        self.fields['brand'].empty_label = "Select a Brand Name"

class ElectronicPurchasingDocumentForm(FileValidatorMixin, forms.ModelForm):
    allowed_extensions = ['pdf']
    class Meta:
        model = ElectronicPurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['po_number'].widget.attrs['placeholder'] = 'Enter a PO Number'
        self.fields['invoice_number'].widget.attrs['placeholder'] = 'Enter an Invoice Number'
        
        self.fields['supplier'].empty_label = "Select a Supplier Name"
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['serial_number'].widget.attrs['placeholder'] = 'Enter a Serial Number'
        self.fields['price_per_unit'].widget.attrs['placeholder'] = 'Enter an Price per Unit'
        self.fields['remark'].widget.attrs['placeholder'] = 'Enter a remark if any'
        
        self.fields['electronic_item'].empty_label = "Select an Electronic Item"
        self.fields['purchasing_document'].empty_label = "Select a related Purchasing Document"
    
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

        self.fields['current_user'].empty_label = "Select a Current User"
        
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
