from django.contrib import admin
from .models import *

class ElectronicUserLocationAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'careholder_name', 'phone_number', 'create_by', 'create_date', 
        'update_date']
    list_filter = ['company_name']

class ElectronicUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'location', 'create_by', 'create_date', 'update_date']
    list_filter = ['location']

class ElectronicBrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'create_by', 'create_date', 'update_date']
    list_filter = ['brand_name']

class ElectronicModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_name', 'create_by', 'create_date', 'update_date']
    list_filter = ['brand']

class ElectronicPurchasingDocumentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'po_number', 'po_doc', 'invoice_number', 'invoice_doc', 'create_by', 
        'create_date', 'update_date']
    list_filter = ['supplier']

class ElectronicInventoryAdmin(admin.ModelAdmin):
    list_display = ['electronic_item', 'serial_number', 'price_per_unit', 'date_of_purchase', 
        'purchasing_document', 'status', 'remark', 'display_previous_user', 'create_by', 'create_date', 
        'update_date']
    list_filter = ['electronic_item__brand']

    def display_previous_user(self, obj):
        return ', '.join([previous_user.name for previous_user in obj.previous_users.all()])
    display_previous_user.short_description = 'Previous Users'

class ElectronicTransactionAdmin(admin.ModelAdmin):
    list_display = ['current_user', 'electronic_item', 'transaction_type', 'initial_agreement_doc', 
        'return_agreement_doc', 'create_by', 'create_date', 'update_date']
    list_filter = ['electronic_item', 'transaction_type']

    
admin.site.register(ElectronicUserLocation, ElectronicUserLocationAdmin)
admin.site.register(ElectronicUser, ElectronicUserAdmin)
admin.site.register(ElectronicBrand, ElectronicBrandAdmin)
admin.site.register(ElectronicModel, ElectronicModelAdmin)
admin.site.register(ElectronicPurchasingDocument, ElectronicPurchasingDocumentAdmin)
admin.site.register(ElectronicInventory, ElectronicInventoryAdmin)
admin.site.register(ElectronicTransaction, ElectronicTransactionAdmin)