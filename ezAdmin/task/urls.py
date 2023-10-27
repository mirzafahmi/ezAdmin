from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task, name = 'task-list'),
    path('task/order_execution_list/create', views.order_execution_add, name = 'task-order-execution'),
    path('task/order_execution_list/create/ajax/', views.ajax_order_execution_add, name = 'task-ajax-order-execution'),
    path('task/order_execution_list/<int:pk>', views.order_execution_details, name = 'task-order-execution-details'),
    path('task/order_execution_list/', views.order_execution_list, name = 'task-order-execution-list'),
    path('task/invoices/', views.invoices, name = 'task-invoices'),
    path('task/proforma_invoices/', views.proforma_invoices, name = 'task-proforma-invoices'),
    path('task/quotation_list/create', views.quotation, name = 'task-quotation'),
    path('task/quotation_list/ajax/', views.ajax_quotation, name = 'task-ajax-quotation'),
    path('task/quotation_list/', views.quotation_details, name = 'task-quotation-list'),
    path('task/quotation_list/quotation_id:<int:pk>-update/', views.quotation_update, name = 'task-quotation-update'),
    path('task/quotation_list/quotation_id:<int:pk>-delete/', views.quotation_delete, name = 'task-quotation-delete'),
    path('task/quotation_list/quotation_id:<int:pk>-pdf/', views.quotation_pdf, name = 'task-quotation-pdf'),
    #path('task/test/', views.generate_pdf, name = 'task-test'),
]
