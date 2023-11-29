from django import forms
from .models import *


class BrandNameForm(forms.ModelForm):
    class Meta:
        model = BrandName
        fields = ['brand_name', 'company_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['brand_name'].widget.attrs['placeholder'] = "Enter Brand name"
        self.fields['company_name'].widget.attrs['placeholder'] = "Enter Brand's company name"
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['identifier', 'item_code', 'name' ,'brand', 'uom', 'packing']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['item_code'].widget.attrs['placeholder'] = "Enter Item Code for the product"
        self.fields['name'].widget.attrs['placeholder'] = "Enter Name for the product"
        self.fields['packing'].widget.attrs['placeholder'] = "Enter the Packing per UOM for the product"

        self.fields['identifier'].empty_label = "Select a Identifier for the product"
        self.fields['brand'].empty_label = "Select a Brand for the product"
        self.fields['uom'].empty_label = "Select a UOM for the product"

        self.fields['identifier'].queryset = self.fields['identifier'].queryset.order_by('parent_item_code')

class InventoryForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product.objects.all(),required = True, disabled = True) 
    class Meta:
        model = FinishedGoodsInventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'stock_type']
