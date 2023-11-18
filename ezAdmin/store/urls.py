from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('store/finished_product/', views.product_list, name = 'store-product'),
    path('store/finished_product/add/', views.product_add, name = 'store-product-add'),
    path('store/finished_product/<int:pk>-update/', views.product_update, name = 'store-product-update'),
    path('store/finished_product/<int:pk>-delete/', views.product_delete, name = 'store-product-delete'),
    path('store/finished_product/<int:pk>-inventory_details/', views.product_inventory_list, name = 'store-product-inventory-list'),
    path('store/finished_product/<int:pk>-inventory_details/add/', views.product_inventory_transaction, name = 'store-product-inventory-add'),
    path('store/finished_product/<int:fk>-inventory_details/<int:pk>-update/', views.product_inventory_update, name = 'store-product-inventory-update'),
    path('store/finished_product/<int:fk>-inventory_details/<int:pk>-delete/', views.product_inventory_delete, name = 'store-product-inventory-delete'),
]