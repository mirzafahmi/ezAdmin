from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('inventory_main/finished_product/', views.product_list, name = 'dashboard-product'),
    path('inventory_main/finished_product/add', views.product_add, name = 'dashboard-product-add'),
    path('inventory_main/finished_product/<int:pk>-update/', views.product_update, name = 'dashboard-product-update'),
    path('inventory_main/finished_product/<int:pk>-delete/', views.product_delete, name = 'dashboard-product-delete'),
    path('inventory_main/finished_product/<int:pk>-inventory_details/', views.product_inventory_list, name = 'dashboard-product-inventory-list'),
    path('inventory_main/finished_product/<int:pk>-inventory_details/add', views.product_inventory_transaction, name = 'dashboard-product-inventory-add'),
    path('inventory_main/finished_product/<int:fk>-inventory_details/<int:pk>-update', views.product_inventory_update, name = 'dashboard-product-inventory-update'),
    path('inventory_main/finished_product/<int:fk>-inventory_details/<int:pk>-delete', views.product_inventory_delete, name = 'dashboard-product-inventory-delete'),
    path('customer_list/', views.customer_list, name = 'dashboard-customer'),
    path('customer_list/add', views.customer_add, name = 'dashboard-customer-add'),
    path('customer_list/<int:pk>-update', views.customer_update, name = 'dashboard-customer-update'),
    path('customer_list/<int:pk>-delete', views.customer_delete, name = 'dashboard-customer-delete'),
]