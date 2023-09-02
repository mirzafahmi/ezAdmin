from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('task/', views.task, name = 'task-list'),
    path('task/delivery_order/', views.delivery_order, name = 'task-delivery-order'),
    path('task/invoices/', views.invoices, name = 'task-invoices'),
    path('task/proforma_invoices/', views.proforma_invoices, name = 'task-proforma-invoices')
]