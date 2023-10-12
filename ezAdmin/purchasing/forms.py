from django import forms
from .models import *

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
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'lot_number', 'exp_date', 'quantity', 'stock_type', 'price_per_unit', 'purchasing_doc']

class RawMaterialInventoryInForm(forms.ModelForm):
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'quantity', 'lot_number', 'exp_date', 'price_per_unit', 'purchasing_doc']
        widgets = {
            'component': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'lot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'exp_date': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'purchasing_doc': forms.Select(attrs={'class': 'form-control'}),
        }

    stock_type = forms.CharField(widget=forms.HiddenInput(), initial='1')  # Set stock_type to '1' for Stock-In

class RawMaterialInventoryOutForm(forms.ModelForm):
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'quantity', 'lot_number', 'exp_date', 'price_per_unit', 'purchasing_doc']
        widgets = {
            'component': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'lot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'exp_date': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'purchasing_doc': forms.Select(attrs={'class': 'form-control'}),
        }

    stock_type = forms.CharField(widget=forms.HiddenInput(), initial='2')  # Set stock_type to '2' for Stock-Out
    stock_in_record = forms.ModelChoiceField(
        queryset=RawMaterialInventory.objects.filter(stock_type='1'),  # Filter only stock-in records
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Stock-In Record'
    )