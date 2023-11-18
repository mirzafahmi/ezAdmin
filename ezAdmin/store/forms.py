from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'name' ,'brand', 'uom', 'packing']

class InventoryForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product.objects.all(),required = True, disabled = True) 
    class Meta:
        model = FinishedGoodsInventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'stock_type']
