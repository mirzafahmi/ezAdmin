from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task, name = 'task-list'),
    path('task/delivery_order/', views.delivery_order, name = 'task-delivery-order'),
    path('task/invoices/', views.invoices, name = 'task-invoices'),
    path('task/proforma_invoices/', views.proforma_invoices, name = 'task-proforma-invoices'),
    path('task/quotation', views.quotation, name = 'task-quotation'),
    path('task/quotation/details', views.quotation_details, name = 'task-quotation-list'),
    path('task/quotation/details/<int:pk>/update', views.quotation_update, name = 'task-quotation-update'),
    path('task/quotation/details/<int:pk>/delete', views.quotation_delete, name = 'task-quotation-delete'),
]
