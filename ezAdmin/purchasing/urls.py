from django.urls import path
from .views import *


urlpatterns = [
    path('purchasing_main', PurchasingMainView.as_view(), name = 'purchasing-main'),
    path('purchasing_main/supplier_list/create', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing_main/supplier_list', SupplierListView.as_view(), name='purchasing-supplier-list'),
    path('purchasing_main/supplier_list/<int:pk>-update/', SupplierUpdateView.as_view(), name='purchasing-supplier-update'),
    path('purchasing_main/supplier_list/<int:pk>-delete/', SupplierDeleteView.as_view(), name='purchasing-supplier-delete'),
    path('purchasing_main/purchasing_document_list/create', PurchasingDocumentCreateView.as_view(), name='purchasing-purchasing-document-create'),
    path('purchasing_main/purchasing_document_list', PurchasingDocumentListView.as_view(), name='purchasing-purchasing-document-list'),
    path('purchasing_main/purchasing_document_list/<int:pk>-update/', PurchasingDocumentUpdateView.as_view(), name='purchasing-purchasing-document-update'),
    path('purchasing_main/purchasing_document_list/<int:pk>-delete/', PurchasingDocumentDeleteView.as_view(), name='purchasing-purchasing-document-delete'),
]