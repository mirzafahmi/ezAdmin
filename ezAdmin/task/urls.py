from django.urls import path
from . import views

urlpatterns = [
    path('task/quotation', views.quotation, name = 'quotation'),
]
