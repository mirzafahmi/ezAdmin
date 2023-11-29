from django import forms
from .models import *
import requests
from mixins.validation_mixin import QuantityValidationMixin
from django.core.exceptions import ValidationError
from django.db.models import F, Sum, Value
from collections import OrderedDict

class RawMaterialIdentifierForm(forms.ModelForm):
    class Meta:
        model = RawMaterialIdentifier
        fields = ['parent_item_code']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent_item_code'].label = "Identifier"

        self.fields['parent_item_code'].widget.attrs['placeholder'] = 'Enter Identifier'

class RawMaterialComponentForm(forms.ModelForm):
    class Meta:
        model = RawMaterialComponent
        fields = ['identifier', 'component', 'spec']
    
    def __init__(self, *args, **kwargs):
        super(RawMaterialComponentForm, self).__init__(*args, **kwargs)

        self.fields['component'].widget.attrs['placeholder'] = 'Enter Component for this identifier'
        self.fields['spec'].widget.attrs['placeholder'] = 'Enter Specification for this component'

        self.fields['identifier'].empty_label = "Select a Identifier"

        identifier_id = self.initial.get('identifier_id') or self.data.get('identifier_id')

        if 'identifier_id' in self.initial:
            self.fields['identifier'].disabled = True
            self.initial['identifier'] = identifier_id
        else:
            self.fields['identifier'].disabled = False
        
        self.fields['identifier'].queryset = self.fields['identifier'].queryset.order_by('parent_item_code')
    
    def clean(self):
        cleaned_data = super().clean()
        component = cleaned_data.get('component')
        identifier = cleaned_data.get('identifier')
        spec = cleaned_data.get('spec')

        if component and identifier and spec:
            # Check if a similar component already exists for the identifier
            similar_components = RawMaterialComponent.objects.filter(
                identifier=identifier,
                component__iexact=component,
                spec__iexact=spec
            ).exclude(pk=self.instance.pk if self.instance else None)

            if similar_components.exists():
                self.add_error("spec", "A similar component with same specification already exists for this identifier.")

        return cleaned_data

class BOMComponentForm(forms.ModelForm):
    class Meta:
        model = BOMComponent
        fields = ['product', 'raw_material_component', 'quantity_used', 'uom']
    
    def __init__(self, *args, **kwargs):
        super(BOMComponentForm, self).__init__(*args, **kwargs)

        # Customize the queryset for the product field to use item_code as the display field
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.item_code}" if obj.item_code else obj.name

        self.fields['quantity_used'].widget.attrs['placeholder'] = 'Enter Quantity Used for this BOMcomponent'

        self.fields['product'].empty_label = "Select a product's item code"
        self.fields['raw_material_component'].empty_label = "Select a raw material component"
        self.fields['uom'].empty_label = "Select a UOM"

        self.fields['raw_material_component'].queryset = self.fields['raw_material_component'].queryset.order_by('identifier__parent_item_code', 'component')

    def clean(self):
        cleaned_data = super().clean()
        component = cleaned_data.get('raw_material_component')
        product = cleaned_data.get('product')

        if component and product:
            # Check if a similar component already exists for the product
            similar_components = BOMComponent.objects.filter(
                product=product,
                raw_material_component=component  # Case-insensitive comparison
            ).exclude(pk=self.instance.pk if self.instance else None)

            if similar_components.exists():
                self.add_error("raw_material_component", "A similar BOMcomponent already exists for this product.")

        return cleaned_data

class ProductionLogForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        empty_label="Select a product's item code",
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    data_overide = forms.BooleanField(required=False)
    class Meta:
        model = ProductionLog
        fields = ['rH', 'temperature', 'BOMComponents', 'lot_number', 'exp_date', 'quantity_produced']
    
    def __init__(self, *args, **kwargs):
        super(ProductionLogForm, self).__init__(*args, **kwargs)

        self.fields['rH'].label = 'Relative Humidity (rH)'
        self.fields['temperature'].label = 'Temperature (°C)'
        self.fields['exp_date'].label = 'Expiry Date'

        self.fields['lot_number'].widget.attrs['placeholder'] = f'In format of ITEMCODEYYMMMDD (Ex.: PRDEN123OCT21)'
        self.fields['exp_date'].widget.attrs['placeholder'] = f'In format of YYYY-MM (Ex.: 2023-10)'
        self.fields['quantity_produced'].widget.attrs['placeholder'] = f'Please enter a Quantity Produced'
        self.fields['rH'].widget.attrs['placeholder'] = f'Please enter a rH value'
        self.fields['temperature'].widget.attrs['placeholder'] = f'Please enter a Temperature value'
        
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['product'].initial = kwargs['instance'].BOMComponents.all()[0].product.id
            self.fields['product'].disabled = True

        self.fields['product'].label_from_instance = lambda obj: f"{obj.item_code}"

        new_fields = OrderedDict()
        new_fields['product'] = self.fields['product']  # Place the 'product' field at the top

        for key in self.fields.keys():
            if key != 'products':
                new_fields[key] = self.fields[key]

        self.fields = new_fields

    def __iter__(self):
        field_order = ['product', 'lot_number', 'exp_date', 'quantity_produced', 'rH', 'temperature', 'BOMComponents', 'data_overide']  # Order of fields you want
        for field_name in field_order:
            yield self[field_name]
    
class RawMaterialInventoryForm(forms.ModelForm, QuantityValidationMixin):
    data_overide = forms.BooleanField(required=False)
    
    class Meta:
        model = RawMaterialInventory
        fields = ['component', 'quantity', 'uom', 'stock_type', 'price_per_unit', 'purchasing_doc', 'lot_number', 'exp_date', 
        'stock_in_tag']
        widgets = {
            'stock_in_tag': forms.HiddenInput(),  # Hide the related_stock_in field
        }

    def __init__(self, *args, **kwargs):
        super(RawMaterialInventoryForm, self).__init__(*args, **kwargs)

        self.fields['quantity'].widget.attrs['placeholder'] = f'Please enter a Quantity'
        self.fields['price_per_unit'].widget.attrs['placeholder'] = f'Please enter a Price per Unit'
        self.fields['lot_number'].widget.attrs['placeholder'] = f'Please enter a Lot Number'
        self.fields['exp_date'].widget.attrs['placeholder'] = f'Please enter a Expiry Date in format of YYYY-MM'

        self.fields['purchasing_doc'].empty_label = "Select a related Purchasing Document"
        self.fields['uom'].empty_label = "Select a UOM"
        
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
        
        #set maximum stock can be log out
        if stock_type == '2':

            #set the dropdown choice based on lot number
            stock_in_tags = RawMaterialInventory.objects.filter(
                    component=component_id,
                    stock_type='1'
                    ).values_list('stock_in_tag', flat=True)
                
            lot_numbers = []

            for stock_in_tag in stock_in_tags:
                stock_in = RawMaterialInventory.objects.filter(
                    stock_type='1', 
                    stock_in_tag=stock_in_tag
                    ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

                stock_out = RawMaterialInventory.objects.filter(
                    stock_type='2', 
                    stock_in_tag=stock_in_tag
                    ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

                balance_stock = stock_in - stock_out

                
                lot_numbers.append(RawMaterialInventory.objects.filter(stock_type='1', stock_in_tag=stock_in_tag).values_list('lot_number', flat=True)[0])

            # Generate choices
            choices = [(num, num) for num in lot_numbers]
            self.fields['lot_number'].widget = forms.Select(choices=choices)

            #set the placeholder quantity
            if not inventory_log:
                available_quantity = self.calculate_available_quantity(component_id)
                self.fields['quantity'].widget.attrs['placeholder'] = f'Maximum quantity available is {available_quantity} pcs' if available_quantity is not None else 'Stock is unavailable'
                
            else:
                lot_number = self.initial.get('lot_number')
                lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number, inventory_log)
                self.fields['quantity'].widget.attrs['placeholder'] = f'Maximum quantity available is {lot_number_balance_stock} pcs' if lot_number_balance_stock is not None else 'Stock is unavailable'
            

        self.initial['component'] = component_id

        #set query dropdown list
        # If stock type is '2', filter the component queryset based on stock-in entries and its related component only
        if stock_type == '2':
            stocked_in_components = RawMaterialInventory.objects.filter(stock_type='1', component__identifier_id = identifier_id).values_list('component_id', flat=True).distinct()
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id__in=stocked_in_components)
            
        else:
            #the comment one is not in used as we cannot filter the inventory models as it dont have componennt id of not stock in componennt
            self.fields['component'].queryset = RawMaterialComponent.objects.filter(id=component_id)

    def calculate_available_quantity(self, component_id, inventory_log = None):
        current_raw_material, current_raw_material_quantity = self.get_available_quantity_fifo(component_id, inventory_log)
        
        return current_raw_material_quantity
    
    def clean(self):
        cleaned_data = super().clean()
        stock_type = cleaned_data.get('stock_type')
        quantity = cleaned_data.get('quantity')
        component = cleaned_data.get('component')
        purchasing_doc = cleaned_data.get('purchasing_doc')
        lot_number = cleaned_data.get('lot_number')
        data_overide = cleaned_data.get('data_overide')
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

            if data_overide:
                component_id = component.id 
                lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number, inventory_log)

                if quantity > lot_number_balance_stock:
                    self.add_error('quantity', f"Quantity exceeds available quantity: {lot_number_balance_stock} unit(s).")

            #innitial create render
            elif not inventory_log:
                component_id = component.id
                lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number, inventory_log)
                if quantity > lot_number_balance_stock if lot_number_balance_stock is not None else 0:
                    self.add_error('quantity', f"Quantity exceeds available quantity: {lot_number_balance_stock} unit(s).")

            else:
                component_id = component.id 
                lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number, inventory_log)
                if quantity > lot_number_balance_stock if lot_number_balance_stock is not None else 0:
                    self.add_error('quantity', f"Quantity exceeds available quantity: {lot_number_balance_stock} unit(s).")


        return cleaned_data
