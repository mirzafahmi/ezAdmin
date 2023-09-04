from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'name' ,'brand', 'uom', 'packing', 'quantity']