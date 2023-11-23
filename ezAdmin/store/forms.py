from django import forms
from .models import *


class BrandNameForm(forms.ModelForm):
    class Meta:
        model = BrandName
        fields = ['brand_name', 'company_name']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['identifier', 'item_code', 'name' ,'brand', 'uom', 'packing']

class InventoryForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product.objects.all(),required = True, disabled = True) 
    class Meta:
        model = FinishedGoodsInventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'stock_type']
