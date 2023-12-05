from django.contrib import admin
from .models import *

# Register your models here.
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency_code', 'create_by', 'create_date', 'update_date']
    list_filter = ['currency_code']

class UOMAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_by', 'create_by', 'create_date', 'update_date']
    list_filter = ['name'] 

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(UOM, UOMAdmin)