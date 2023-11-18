from django.contrib import admin
from production.views import *
# Register your models here.

class RawMaterialIdentifierAdmin(admin.ModelAdmin):
    list_display = ['parent_item_code']
    list_filter = ['parent_item_code']

class RawMaterialComponentAdmin(admin.ModelAdmin):
    list_display = ['component', 'spec', 'identifier']
    list_filter = ['component']

class BOMComponentAdmin(admin.ModelAdmin):
    list_display = ['product', 'raw_material_component', 'quantity_used']
    list_filter = ['product', 'raw_material_component']

class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ['display_item_code', 'rH', 'temperature','display_bom_components', 'lot_number', 'exp_date', 'quantity_produced',]
    list_filter = ['lot_number']

    fieldsets = (
        ('Item Code', {
            'fields': ('display_item_code',),  # Add the new field here
        }),
        ('General', {
            'fields': ('lot_number', 'exp_date', 'quantity_produced', 'BOMComponents', 'rH', 'temperature', 'create_date', 'update_date'),
        }),
    )

    readonly_fields = ('display_item_code',)

    def display_bom_components(self, obj):
        return ', '.join([bom_component.raw_material_component.component for bom_component in obj.BOMComponents.all()])
    display_bom_components.short_description = 'BOM Components'

    def display_item_code(self, obj):
        return ', '.join([obj.BOMComponents.all()[0].product.item_code])
    display_item_code.short_description = 'Item Code'


class RawMaterialInventoryAdmin(admin.ModelAdmin):
    list_display = ['component', 'quantity', 'stock_type', 'price_per_unit', 'purchasing_doc', 'lot_number', 'exp_date', 'production_log']
    list_filter = ['component', 'stock_type', 'purchasing_doc']


admin.site.register(RawMaterialIdentifier, RawMaterialIdentifierAdmin)
admin.site.register(RawMaterialComponent, RawMaterialComponentAdmin)
admin.site.register(BOMComponent, BOMComponentAdmin)
admin.site.register(ProductionLog, ProductionLogAdmin)
admin.site.register(RawMaterialInventory, RawMaterialInventoryAdmin)

