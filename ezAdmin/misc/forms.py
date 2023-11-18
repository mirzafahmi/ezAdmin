from django import forms
from .models import *

class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = ['name']

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name', 'currency_code']