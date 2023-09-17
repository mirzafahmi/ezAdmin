from django.contrib import admin
from .models import *

admin.site.site_header = 'ezAdmin Administrative Dashboard View'

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'create_date', 'update_date']
    list_filter = ['brand_name']

class SalesAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'update_date']
    list_filter = ['name']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency_code', 'create_date', 'update_date']
    list_filter = ['currency_code']

class UOMAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'update_date']
    list_filter = ['name']    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'name', 'brand', 'packing', 'uom', 'create_date', 'update_date')
    list_filter = ['brand']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'stock_in_date', 'stock_out_date')
    list_filter = ['quantity']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'email', 'sales_person', 'address', 'posscode', 'create_date', 'update_date')
    list_filter = ['sales_person']

class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative', 'price_KG', 'payment_term']
    list_filter = ['name']

class QuotationAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'doc_number']
    list_filter = ['customer_id']

class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'product', 'price', 'quantity']
    list_filter = ['quotation']

class OrderExecutionAdmin(admin.ModelAdmin):
    list_display = ['quotation_id', 'do_number','inv_number', 'delivery_method', 'tracking_number', 'create_date']
    list_filter = ['create_date', 'delivery_method',]

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BrandName, BrandAdmin)
admin.site.register(SalesPerson, SalesAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(UOM, UOMAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(Quotation, QuotationAdmin)
admin.site.register(QuotationItem, QuotationItemAdmin)
admin.site.register(OrderExecution, OrderExecutionAdmin)