from django.urls import path
from . import views
from django.views.generic import TemplateView


'''
breadcrumbs = Breadcrumbs(
    ("Home", "/"),
    ("Inventory Main Page", "/inventory/main/"),
    ("Raw Material Inventory Main Page", "/inventory/raw_material/main/"),
)'''

urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('inventory_main/finished_product/', views.product_list, name = 'dashboard-product'),
    path('inventory/finished-product/add', views.product_add, name = 'dashboard-product-add'),
    path('inventory/finished-product/update/<int:pk>/', views.product_update, name = 'dashboard-product-update'),
    path('inventory/finished-product/delete/<int:pk>/', views.product_delete, name = 'dashboard-product-delete'),
    path('inventory/finished-product/details/<int:pk>/', views.product_inventory_list, name = 'dashboard-product-inventory-list'),
    path('inventory/finished-product/details/<int:pk>/inventory-add', views.product_inventory_transaction, name = 'dashboard-product-inventory-add'),
    path('inventory/finished-product/details/<int:fk>/inventory-update/<int:pk>', views.product_inventory_update, name = 'dashboard-product-inventory-update'),
    path('inventory/finished-product/details/<int:fk>/inventory-delete/<int:pk>', views.product_inventory_delete, name = 'dashboard-product-inventory-delete'),
    path('customer/', views.customer_list, name = 'dashboard-customer'),
    path('customer/add', views.customer_add, name = 'dashboard-customer-add'),
    path('customer/update/<int:pk>', views.customer_update, name = 'dashboard-customer-update'),
    path('customer/delete/<int:pk>', views.customer_delete, name = 'dashboard-customer-delete'),
]