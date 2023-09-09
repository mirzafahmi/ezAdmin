from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('product/', views.product_list, name = 'dashboard-product'),
    path('product/add', views.product_add, name = 'dashboard-product-add'),
    path('product/update/<int:pk>/', views.product_update, name = 'dashboard-product-update'),
    path('product/delete/<int:pk>/', views.product_delete, name = 'dashboard-product-delete'),
    path('product/details/<int:pk>/', views.product_inventory_list, name = 'dashboard-product-inventory-list'),
    path('product/details/<int:pk>/inventory-add', views.product_inventory_transaction, name = 'dashboard-product-inventory-add'),
    path('product/details/<int:fk>/inventory-update/<int:pk>', views.product_inventory_update, name = 'dashboard-product-inventory-update'),
    path('product/details/<int:fk>/inventory-delete/<int:pk>', views.product_inventory_delete, name = 'dashboard-product-inventory-delete'),
    path('customer/', views.customer_list, name = 'dashboard-customer'),
    path('customer/add', views.customer_add, name = 'dashboard-customer-add'),
    path('customer/update/<int:pk>', views.customer_update, name = 'dashboard-customer-update'),
    path('customer/delete/<int:pk>', views.customer_delete, name = 'dashboard-customer-delete'),
]