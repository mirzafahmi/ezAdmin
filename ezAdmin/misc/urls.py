from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('misc_main/', MiscMainView.as_view(), name = 'misc-main'),
    path('misc_main/uom_list/', UOMListView.as_view(), name='misc-uom-list'),
    path('misc_main/uom_list/create', UOMCreateView.as_view(), name='misc-uom-create'),
    path('misc_main/uom_list/UOM:<int:pk>-update', UOMUpdateView.as_view(), name='misc-uom-update'),
    path('misc_main/uom_list/UOM:<int:pk>-delete', UOMDeleteView.as_view(), name='misc-uom-delete'),
    path('misc_main/currency_list/', CurrencyListView.as_view(), name='misc-currency-list'),
    path('misc_main/currency_list/create', CurrencyCreateView.as_view(), name='misc-currency-create'),
    path('misc_main/currency_list/currency:<int:pk>-update', CurrencyUpdateView.as_view(), name='misc-currency-update'),
    path('misc_main/currency_list/currency:<int:pk>-delete', CurrencyDeleteView.as_view(), name='misc-currency-delete'),
]