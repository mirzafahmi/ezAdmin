from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'name' ,'brand', 'uom', 'packing']

class InventoryForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset = Product.objects.all(),required = True, disabled = True) 
    class Meta:
        model = Inventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'type']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'posscode', 'pic_name', 'phone_number', 'email', 'currency', 'sales_person']

class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = ['name']

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name', 'currency_code']
