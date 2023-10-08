from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('purchasing/main', TemplateView.as_view(template_name = 'purchasing/purchasing_main.html'), name = 'purchasing-main'),
    path('purchasing/supplier/create', SupplierCreateView.as_view(), name='purchasing-supplier-create'),
    path('purchasing/supplier/list', SupplierListView.as_view(), name='purchasing-supplier-list'),
    path('purchasing/supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='purchasing-supplier-update'),
    path('purchasing/supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='purchasing-supplier-delete'),
    path('purchasing/purchasing_document/create', PurchasingDocumentCreateView.as_view(), name='purchasing-purchasing-document-create'),
    path('purchasing/purchasing_document/list', PurchasingDocumentListView.as_view(), name='purchasing-purchasing-document-list'),
    path('purchasing/purchasing_document/<int:pk>/update/', PurchasingDocumentUpdateView.as_view(), name='purchasing-purchasing-document-update'),
    path('purchasing/purchasing_document/<int:pk>/delete/', PurchasingDocumentDeleteView.as_view(), name='purchasing-purchasing-document-delete'),
    path('purchasing/raw_material_identifier/create', RawMaterialIdentifierCreateView.as_view(), name='purchasing-raw-material-identifier-create'),
    path('purchasing/raw_material_identifier/list', RawMaterialIdentifierListView.as_view(), name='purchasing-raw-material-identifier-list'),
    path('purchasing/raw_material_identifier/<int:pk>/update/', RawMaterialIdentifierUpdateView.as_view(), name='purchasing-raw-material-identifier-update'),
    path('purchasing/raw_material_identifier/<int:pk>/delete/', RawMaterialIdentifierDeleteView.as_view(), name='purchasing-raw-material-identifier-delete'),
]