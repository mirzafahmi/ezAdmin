from django import forms
from .models import *
import requests
from mixins.validation_mixin import QuantityValidationMixin

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'address', 'representative_name', 'phone_number', 'email', 'currency_trade']

class PurchasingDocumentForm(forms.ModelForm):
    class Meta:
        model = PurchasingDocument
        fields = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc', 'AWB_number', 'AWB_doc']
        
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

class RawMaterialInventoryForm(forms.ModelForm, QuantityValidationMixin):
    data_overide = forms.BooleanField(required=False)
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'quantity', 'stock_type', 'price_per_unit', 'purchasing_doc', 'lot_number', 'exp_date']

    def __init__(self, *args, **kwargs):
        super(RawMaterialInventoryForm, self).__init__(*args, **kwargs)
        self.fields['lot_number'].required = False
        self.fields['exp_date'].required = False

        if 'component_id' in self.initial:
            self.fields['component'].disabled = True
        if 'stock_type' in self.initial:
            self.fields['stock_type'].disabled = True
        
        # Get the stock type from the initial data or the form data
        stock_type = self.initial.get('stock_type') or self.data.get('stock_type')
        identifier_id = self.initial.get('identifier_id') or self.data.get('identifier_id')
        component_id = self.initial.get('component_id') or self.data.get('component_id')
        inventory_log = getattr(self, 'instance', None).pk
        
        if stock_type == '2':
            if not inventory_log:
                available_quantity = self.calculate_available_quantity(component_id)
                self.fields['quantity'].widget.attrs['placeholder'] = f'Maximum quantity available is {available_quantity} pcs' if available_quantity is not None else 'Stock is unavailable'
                
            else:
                available_quantity = self.calculate_available_quantity(component_id, inventory_log)
                self.fields['quantity'].widget.attrs['placeholder'] = f'Maximum quantity available is {available_quantity} pcs' if available_quantity is not None else 'Stock is unavailable'
            

        self.initial['component'] = component_id

        # If stock type is '2', filter the component queryset based on stock-in entries and its related component only
        if stock_type == '2':
            stocked_in_components = RawMaterialInventory.objects.filter(stock_type='1', component__identifier_id = identifier_id).values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)
    
        else:
            stocked_in_components = RawMaterialInventory.objects.filter(component__identifier_id = identifier_id).values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)

    def calculate_available_quantity(self, component_id, inventory_log = None):
        current_raw_material, current_raw_material_quantity = self.get_available_quantity(component_id, inventory_log)
        return current_raw_material_quantity

    def clean(self):
        cleaned_data = super().clean()
        stock_type = cleaned_data.get('stock_type')
        quantity = cleaned_data.get('quantity')
        component = cleaned_data.get('component')
        purchasing_doc = cleaned_data.get('purchasing_doc')
        lot_number = cleaned_data.get('lot_number')
        inventory_log = getattr(self, 'instance', None).pk

        # If stock_type is '1' (Stock In), ensure lot_number and exp_date are provided
        if stock_type == '1':
            if not lot_number:
                self.add_error('lot_number', 'Lot Number is required for Stock In.')
            if not lot_number:
                self.add_error('exp_date', 'Expiry Date is required for Stock In.')
            if quantity <= 0:
                self.add_error('quantity', "Stock in quantity must be more than 0.")
        else:
            if quantity <= 0:
                self.add_error('quantity', "Stock out quantity must be more than 0.")
            
            if not inventory_log:
                component_id = component.id  # Assuming component has an 'id' field
                available_quantity = self.calculate_available_quantity(component_id)
                if quantity > available_quantity if available_quantity is not None else 0:
                    self.add_error('quantity', "Quantity exceeds available quantity.")
            else:
                component_id = component.id  # Assuming component has an 'id' field
                available_quantity = self.calculate_available_quantity(component_id, inventory_log)
                if quantity > available_quantity if available_quantity is not None else 0:
                    self.add_error('quantity', "Quantity exceeds available quantity.")
            
        return cleaned_data
