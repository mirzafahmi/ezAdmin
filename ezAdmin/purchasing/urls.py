from django.urls import path
from .views import *

urlpatterns = [
    path('purchasing/create_supplier/', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing/supplier_list/', SupplierListView.as_view(), name='purchasing-supplier-list'),
]