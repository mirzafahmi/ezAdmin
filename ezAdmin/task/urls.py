from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task, name = 'task-list'),
    path('task/order_execution/add/', views.order_execution_add, name = 'task-order-execution'),
    path('task/order_execution/add/ajax', views.ajax_order_execution_add, name = 'task-ajax-order-execution'),
    path('task/order_execution/<int:pk>', views.order_execution_details, name = 'task-order-execution-details'),
    path('task/order_execution/list', views.order_execution_list, name = 'task-order-execution-list'),
    path('task/invoices/', views.invoices, name = 'task-invoices'),
    path('task/proforma_invoices/', views.proforma_invoices, name = 'task-proforma-invoices'),
    path('task/quotation', views.quotation, name = 'task-quotation'),
    path('task/quotation/ajax', views.ajax_quotation, name = 'task-ajax-quotation'),
    path('task/quotation/details', views.quotation_details, name = 'task-quotation-list'),
    path('task/quotation/details/<int:pk>/update', views.quotation_update, name = 'task-quotation-update'),
    path('task/quotation/details/<int:pk>/delete', views.quotation_delete, name = 'task-quotation-delete'),
    path('task/test/', views.test, name = 'task-test'),
]
