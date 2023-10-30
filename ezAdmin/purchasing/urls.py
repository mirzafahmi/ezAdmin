from django.urls import path
from .views import *


urlpatterns = [
    path('purchasing_main', PurchasingMainView.as_view(), name = 'purchasing-main'),
    path('purchasing_main/supplier_list/create', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing_main/supplier_list', SupplierListView.as_view(), name='purchasing-supplier-list'),
    path('purchasing_main/supplier_list/<int:pk>-update/', SupplierUpdateView.as_view(), name='purchasing-supplier-update'),
    path('purchasing_main/supplier_list/<int:pk>-delete/', SupplierDeleteView.as_view(), name='purchasing-supplier-delete'),
    path('purchasing_main/purchasing_document_list/create', PurchasingDocumentCreateView.as_view(), name='purchasing-purchasing-document-create'),
    path('purchasing_main/purchasing_document_list', PurchasingDocumentListView.as_view(), name='purchasing-purchasing-document-list'),
    path('purchasing_main/purchasing_document_list/<int:pk>-update/', PurchasingDocumentUpdateView.as_view(), name='purchasing-purchasing-document-update'),
    path('purchasing_main/purchasing_document_list/<int:pk>-delete/', PurchasingDocumentDeleteView.as_view(), name='purchasing-purchasing-document-delete'),
    path('production_main', RawMaterialMainView.as_view(), name = 'dashboard-inventory-raw-material-main'),
    path('production_main/raw_material_identifier_list/create', RawMaterialIdentifierCreateView.as_view(), name='purchasing-raw-material-identifier-create'),
    path('production_main/raw_material_identifier_list', RawMaterialIdentifierListView.as_view(), name='purchasing-raw-material-identifier-list'),
    path('production_main/raw_material_identifier_list/<int:pk>-update/', RawMaterialIdentifierUpdateView.as_view(), name='purchasing-raw-material-identifier-update'),
    path('production_main/raw_material_identifier_list/<int:pk>-delete/', RawMaterialIdentifierDeleteView.as_view(), name='purchasing-raw-material-identifier-delete'),
    path('production_main/raw_material_component_list/create', RawMaterialComponentCreateView.as_view(), name='purchasing-raw-material-component-create'),
    path('production_main/raw_material_component_list', RawMaterialComponentListView.as_view(), name='purchasing-raw-material-component-list'),
    path('production_main/raw_material_component_list/<int:pk>-update/', RawMaterialComponentUpdateView.as_view(), name='purchasing-raw-material-component-update'),
    path('production_main/raw_material_component_list/<int:pk>-delete/', RawMaterialComponentDeleteView.as_view(), name='purchasing-raw-material-component-delete'),
    path('production_main/BOM_component_list/create', BOMComponentCreateView.as_view(), name='purchasing-BOM-component-create'),
    path('production_main/BOM_component_list', BOMComponentListView.as_view(), name='purchasing-BOM-component-list'),
    path('production_main/BOM_component_list/<int:pk>-update/', BOMComponentUpdateView.as_view(), name='purchasing-BOM-component-update'),
    path('production_main/BOM_component_list/<int:pk>-delete/', BOMComponentDeleteView.as_view(), name='purchasing-BOM-component-delete'),
    #path('production_main', RawMaterialInventoryLogMainView.as_view(), name = 'purchasing-raw-material-inventory-main'),
    path('inventory_main', InventoryMainView.as_view(), name = 'dashboard-inventory-main'),
    path('production_main/raw_material_inventory_main/create', RawMaterialInventoryCreateView.as_view(), name='purchasing-raw-material-inventory-create'),
    #path('production_main/raw_material_inventory_main/ajax', RawMaterialInventoryAJAX.as_view(), name='purchasing-raw-material-inventory-ajax'),
    #path('production_main/raw_material_inventory_main/list', RawMaterialInventoryListView.as_view(), name='purchasing-raw-material-inventory-list'),
    #path('production_main/raw_material_inventory/<int:pk>-update/', RawMaterialInventoryUpdateView.as_view(), name='purchasing-raw-material-inventory-update'),
    #path('production_main/raw_material_inventory/<int:pk>-delete/', RawMaterialInventoryDeleteView.as_view(), name='purchasing-raw-material-inventory-delete'),
    path('production_main/raw_material_inventory_identifier_based_main', RawMaterialInventoryIdentifierBasedListView.as_view(), name='purchasing-raw-material-inventory-identifier-based-list'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier_create', RawMaterialIdentifierCreateView.as_view(), name='purchasing-raw-material-identifier-list-identifier-create'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main', RawMaterialInventoryIdentifierComponentBasedListView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-list'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component_create', RawMaterialComponentCreateView.as_view(), name='purchasing-raw-material-inventory-identifier-based-component-create'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component:<int:component_id>-list/inventory_log_create_main/create-stock_type:<str:stock_type>', RawMaterialInventoryIdentifierComponentBasedLogCreateView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-create'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier_component_based/create/stock_type/ajax', RawMaterialInventoryIdentifierComponentBasedLogCreateAJAX.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-create-ajax'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component:<int:component_id>-list/inventory_log_create_main', RawMaterialInventoryIdentifierComponentBasedLogCreateMainView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-create-main'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component:<int:component_id>-list', RawMaterialInventoryIdentifierComponentBasedLogListView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-list'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier_component_based/component-list-ajax', RawMaterialInventoryIdentifierComponentBasedLogListViewAJAX.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-list-ajax'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component:<int:component_id>-list/inventory_log_create_main/stock_type:<str:stock_type>-log:<int:pk>-update', RawMaterialInventoryIdentifierComponentBasedLogUpdateView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-update'),
    path('production_main/raw_material_inventory_identifier_based_main/identifier:<int:identifier_id>-component-main/component:<int:component_id>-list/inventory_log_create_main/stock_type:<str:stock_type>-log:<int:pk>-delete', RawMaterialInventoryIdentifierComponentBasedLogDeleteView.as_view(), name='purchasing-raw-material-inventory-identifier-component-based-log-delete'),
]