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

        # If stock type is '2', filter the component queryset based on stock-in entries
        if stock_type == '2':
            stocked_in_components = RawMaterialInventory.objects.filter(stock_type='1').values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)
        else:
            # If stock type is '1' or other, don't apply any additional filtering
            self.fields['component'].queryset = RawMaterialComponent.objects.all()


    def clean(self):
        cleaned_data = super().clean()
        stock_type = cleaned_data.get('stock_type')

        # If stock_type is '1' (Stock In), ensure lot_number and exp_date are provided
        if stock_type == '1':
            if not cleaned_data.get('lot_number'):
                self.add_error('lot_number', 'This field is required for Stock In.')
            if not cleaned_data.get('exp_date'):
                self.add_error('exp_date', 'This field is required for Stock In.')

        return cleaned_data

    '''def clean(self):
        cleaned_data = super().clean()
        stock_type = cleaned_data.get('stock_type')

        if stock_type == '2':  # Stock-Out
            component_id = cleaned_data.get('component').id

            # Fetch FIFO stocks using AJAX to update lot_number and exp_date fields
            fifo_stocks = self.fetch_fifo_stocks(component_id)
            cleaned_data['fifo_stocks'] = fifo_stocks

        return cleaned_data

    def fetch_fifo_stocks(self, component_id):
        # Replace 'http://localhost:8000/get_fifo_stocks/' with your actual endpoint
        url = f'http://localhost:8000/get_fifo_stocks/?component_id={component_id}'
        response = requests.get(url)
        data = response.json()
        return data.get('fifo_stocks', [])'''

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