from django.contrib import admin
from .models import *

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'create_date', 'update_date']
    list_filter = ['brand_name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'name', 'brand', 'packing', 'uom', 'create_date', 'update_date')
    list_filter = ['brand']

admin.site.register(Product, ProductAdmin)
admin.site.register(BrandName, BrandAdmin)