from django.urls import path
from .views import *

urlpatterns = [
    path('purchasing/supplier/create', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing/supplier/list', SupplierListView.as_view(), name='purchasing-supplier-list'),
    path('purchasing/supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='purchasing-supplier-update'),
    path('purchasing/supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='purchasing-supplier-delete'),
    path('purchasing/purchasing_document/create', PurchasingDocumentCreateView.as_view(), name='purchasing-purchasing-document-create'),
    path('purchasing/purchasing_document/list', PurchasingDocumentListView.as_view(), name='purchasing-purchasing-document-list'),
]