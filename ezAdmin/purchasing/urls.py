from django.urls import path
from .views import *

urlpatterns = [
    path('purchasing/create_supplier/', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing/supplier_list/', SupplierListView.as_view(), name='purchasing-supplier-list'),
    path('purchasing/supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='purchasing-supplier-update'),
    path('purchasing/supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='purchasing-supplier-delete'),
]