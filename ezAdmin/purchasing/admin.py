from django.contrib import admin
from .models import *

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'address', 'representative_name', 'phone_number', 'email', 'create_date', 'update_date']
    list_filter = ['company_name']

class PurchasingDocumentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'packing_list', 'pl_doc', 'k1_form', 'k1_doc', 'create_date', 'update_date']
    list_filter = ['supplier__company_name']

class RawMaterialIdentifierAdmin(admin.ModelAdmin):
    list_display = ['parent_item_code']
    list_filter = ['parent_item_code']

class RawMaterialComponentAdmin(admin.ModelAdmin):
    list_display = ['component', 'spec', 'identifier']
    list_filter = ['component']

class BOMComponentAdmin(admin.ModelAdmin):
    list_display = ['product', 'raw_material_component', 'quantity_used']
    list_filter = ['product', 'raw_material_component']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(PurchasingDocument, PurchasingDocumentAdmin)
admin.site.register(RawMaterialIdentifier, RawMaterialIdentifierAdmin)
admin.site.register(RawMaterialComponent, RawMaterialComponentAdmin)
admin.site.register(BOMComponent, BOMComponentAdmin)
