from django.contrib import admin
from .models import BrandName, SalesPerson, Currency, UOM, Product, Customer, DeliveryMethod, Inquiry, OrderExecution

admin.site.site_header = 'ezAdmin Administrative Dashboard View'

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'create_date']
    list_filter = ['brand_name']

class SalesAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date']
    list_filter = ['name']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

class UOMAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'name', 'brand', 'packing', 'uom', 'quantity')
    list_filter = ['brand']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'sales_person', 'address', 'posscode')
    list_filter = ['sales_person']

class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative', 'price_KG', 'payment_term']
    list_filter = ['name']

class InquiryAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'product_id', 'doc_number', 'price_per_unit', 'quantity']
    list_filter = ['customer_id', 'product_id',]

class OrderExecutionAdmin(admin.ModelAdmin):
    list_display = ['inquiry_id', 'doc_number', 'delivery_method', 'tracking_number', 'create_date']
    list_filter = ['create_date', 'delivery_method',]

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BrandName, BrandAdmin)
admin.site.register(SalesPerson, SalesAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(UOM, UOMAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(Inquiry, InquiryAdmin)
#admin.site.register(OrderExecution, OrderExecutionAdmin)