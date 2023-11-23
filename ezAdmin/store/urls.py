from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('store_brand', StoreMainView.as_view(), name='store-main'),
    path('store_brand/brand_name/create', BrandNameCreateView.as_view(), name='store-brand-name-create'),
    path('store_brand/brand_name', BrandNameListView.as_view(), name='store-brand-name-list'),
    path('store_brand/brand_name/<int:pk>-update/', BrandNameUpdateView.as_view(), name='store-brand-name-update'),
    path('store_brand/brand_name/<int:pk>-delete/', BrandNameDeleteView.as_view(), name='store-brand-name-delete'),
    path('store_brand/product_list/', ProductListView.as_view(), name = 'store-product-list'),
    path('store_brand/product_list/create/', ProductCreateView.as_view(), name = 'store-product-add'),
    path('store_brand/product_list/<int:pk>-update/', ProductUpdateView.as_view(), name = 'store-product-update'),
    path('store_brand/product_list/<int:pk>-delete/', ProductDeleteView.as_view(), name = 'store-product-delete'),
    #path('store_brand/finished_product/', views.product_list, name = 'store-product-list'),
    #path('store_brand/finished_product/add/', views.product_create, name = 'store-product-add'),
    #path('store_brand/finished_product/<int:pk>-update/', views.product_update, name = 'store-product-update'),
    #path('store_brand/finished_product/<int:pk>-delete/', views.product_delete, name = 'store-product-delete'),
    path('store_brand/finished_product/<int:pk>-inventory_details/', views.product_inventory_list, name = 'store-product-inventory-list'),
    path('store_brand/finished_product/<int:pk>-inventory_details/add/', views.product_inventory_transaction, name = 'store-product-inventory-add'),
    path('store_brand/finished_product/<int:fk>-inventory_details/<int:pk>-update/', views.product_inventory_update, name = 'store-product-inventory-update'),
    path('store_brand/finished_product/<int:fk>-inventory_details/<int:pk>-delete/', views.product_inventory_delete, name = 'store-product-inventory-delete'),
]