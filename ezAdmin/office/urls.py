from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('office_main', OfficeMainView.as_view(), name = 'office-main'),
    path('office_main/electronic_user_location/create', ElectronicUserLocationCreateView.as_view(), name='office-electronic-user-location-create'),
    path('office_main/electronic_user_location', ElectronicUserLocationListView.as_view(), name='office-electronic-user-location-list'),
    path('office_main/electronic_user_location/<int:pk>-update/', ElectronicUserLocationUpdateView.as_view(), name='office-electronic-user-location-update'),
    path('office_main/electronic_user_location/<int:pk>-delete/', ElectronicUserLocationDeleteView.as_view(), name='office-electronic-user-location-delete'),
    path('office_main/electronic_user/create', ElectronicUserCreateView.as_view(), name='office-electronic-user-create'),
    path('office_main/electronic_user', ElectronicUserListView.as_view(), name='office-electronic-user-list'),
    path('office_main/electronic_user/<int:pk>-update/', ElectronicUserUpdateView.as_view(), name='office-electronic-user-update'),
    path('office_main/electronic_user/<int:pk>-delete/', ElectronicUserDeleteView.as_view(), name='office-electronic-user-delete'),
    path('office_main/electronic_brand/create', ElectronicBrandCreateView.as_view(), name='office-electronic-brand-create'),
    path('office_main/electronic_brand', ElectronicBrandListView.as_view(), name='office-electronic-brand-list'),
    path('office_main/electronic_brand/<int:pk>-update/', ElectronicBrandUpdateView.as_view(), name='office-electronic-brand-update'),
    path('office_main/electronic_brand/<int:pk>-delete/', ElectronicBrandDeleteView.as_view(), name='office-electronic-brand-delete'),
    path('office_main/electronic_model/create', ElectronicModelCreateView.as_view(), name='office-electronic-model-create'),
    path('office_main/electronic_model', ElectronicModelListView.as_view(), name='office-electronic-model-list'),
    path('office_main/electronic_model/<int:pk>-update/', ElectronicModelUpdateView.as_view(), name='office-electronic-model-update'),
    path('office_main/electronic_model/<int:pk>-delete/', ElectronicModelDeleteView.as_view(), name='office-electronic-model-delete'),
    path('office_main/electronic_purchasing_document/create', ElectronicPurchasingDocumentCreateView.as_view(), name='office-electronic-purchasing-document-create'),
    path('office_main/electronic_purchasing_document', ElectronicPurchasingDocumentListView.as_view(), name='office-electronic-purchasing-document-list'),
    path('office_main/electronic_purchasing_document/<int:pk>-update/', ElectronicPurchasingDocumentUpdateView.as_view(), name='office-electronic-purchasing-document-update'),
    path('office_main/electronic_purchasing_document/<int:pk>-delete/', ElectronicPurchasingDocumentDeleteView.as_view(), name='office-electronic-purchasing-document-delete'),
    path('office_main/electronic_inventory/create', ElectronicInventoryCreateView.as_view(), name='office-electronic-inventory-create'),
    path('office_main/electronic_inventory', ElectronicInventoryListView.as_view(), name='office-electronic-inventory-list'),
    path('office_main/electronic_inventory_ajax', ElectronicInventoryListViewAJAX.as_view(), name='office-electronic-inventory-list-ajax'),
    path('office_main/electronic_inventory/<int:pk>-update/', ElectronicInventoryUpdateView.as_view(), name='office-electronic-inventory-update'),
    path('office_main/electronic_inventory/<int:pk>-delete/', ElectronicInventoryDeleteView.as_view(), name='office-electronic-inventory-delete'),
    path('office_main/electronic_transaction/create', ElectronicTransactionCreateView.as_view(), name='office-electronic-transaction-create'),
    path('office_main/electronic_transaction', ElectronicTransactionListView.as_view(), name='office-electronic-transaction-list'),
    path('office_main/electronic_transaction/<int:pk>-update/', ElectronicTransactionUpdateView.as_view(), name='office-electronic-transaction-update'),
    path('office_main/electronic_transaction/<int:pk>-delete/', ElectronicTransactionDeleteView.as_view(), name='office-electronic-transaction-delete'),
]