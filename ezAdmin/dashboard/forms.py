from django import forms
from .models import Product, Inventory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'name' ,'brand', 'uom', 'packing']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'type']