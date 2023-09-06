from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('task/', views.task, name = 'task-list'),
    path('task/delivery_order/', views.delivery_order, name = 'task-delivery-order'),
    path('task/invoices/', views.invoices, name = 'task-invoices'),
    path('task/proforma_invoices/', views.proforma_invoices, name = 'task-proforma-invoices'),
    path('product/', views.product_list, name = 'dashboard-product'),
    path('product/details/<int:pk>/', views.product_details, name = 'dashboard-product-details'),
    path('product/add', views.product_add, name = 'dashboard-product-add'),
    path('product/update/<int:pk>/', views.product_update, name = 'dashboard-product-update'),
    path('product/delete/<int:pk>/', views.product_delete, name = 'dashboard-product-delete')
]