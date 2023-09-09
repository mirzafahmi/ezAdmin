from django import forms
from .models import Product, Inventory, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'name' ,'brand', 'uom', 'packing']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product','quantity', 'lot_number', 'expiry_date', 'quantity', 'type']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'address', 'posscode', 'pic_name', 'phone_number', 'email', 'currency', 'sales_person']