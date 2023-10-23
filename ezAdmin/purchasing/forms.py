from django import forms
from .models import *
import requests

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'address', 'representative_name', 'phone_number', 'email']

class PurchasingDocumentForm(forms.ModelForm):
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc']
        
class RawMaterialIdentifierForm(forms.ModelForm):
    class Meta:
        model = RawMaterialIdentifier
        fields = ['parent_item_code']

class RawMaterialComponentForm(forms.ModelForm):
    class Meta:
        model = RawMaterialComponent
        fields = ['component', 'spec', 'identifier']

class BOMComponentForm(forms.ModelForm):
    class Meta:
        model = BOMComponent
        fields = ['product', 'raw_material_component', 'quantity_used']

class RawMaterialInventoryForm(forms.ModelForm):
    data_overide = forms.BooleanField(required=False)
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'quantity', 'stock_type', 'price_per_unit', 'purchasing_doc', 'lot_number', 'exp_date']

    def __init__(self, *args, **kwargs):
        super(RawMaterialInventoryForm, self).__init__(*args, **kwargs)
        self.fields['lot_number'].required = False
        self.fields['exp_date'].required = False

        if 'stock_type' in self.initial:
            self.fields['stock_type'].disabled = True

        # Get the stock type from the initial data or the form data
        stock_type = self.initial.get('stock_type') or self.data.get('stock_type')
        identifier_id = self.initial.get('identifier_id') or self.data.get('identifier_id')
        component_id = self.initial.get('component_id') or self.data.get('component_id')

        # If stock type is '2', filter the component queryset based on stock-in entries and its related component only
        if stock_type == '2':
            stocked_in_components = RawMaterialInventory.objects.filter(stock_type='1', component__identifier_id = identifier_id).values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)
    
        else:
            stocked_in_components = RawMaterialInventory.objects.filter(component__identifier_id = identifier_id).values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)


    def clean(self):
        cleaned_data = super().clean()
        stock_type = cleaned_data.get('stock_type')
        quantity = cleaned_data.get('quantity')
        component = cleaned_data.get('component')
        purchasing_doc = cleaned_data.get('purchasing_doc')
        lot_number = cleaned_data.get('lot_number')

        # If stock_type is '1' (Stock In), ensure lot_number and exp_date are provided
        if stock_type == '1':
            if not cleaned_data.get('lot_number'):
                self.add_error('lot_number', 'This field is required for Stock In.')
            if not cleaned_data.get('exp_date'):
                self.add_error('exp_date', 'This field is required for Stock In.')
        

        return cleaned_data
