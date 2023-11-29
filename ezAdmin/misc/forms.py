from django import forms
from .models import *

class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = ['name', 'unit', 'weightage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = f"Enter a UOM name"
        self.fields['unit'].widget.attrs['placeholder'] = f"Enter a UOM unit"
        self.fields['weightage'].widget.attrs['placeholder'] = f"Enter a UOM weightage"

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name', 'currency_code']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = f"Enter a Currency name"
        self.fields['currency_code'].widget.attrs['placeholder'] = f"Enter a Currency Code (E.g.: MYR, USD)"