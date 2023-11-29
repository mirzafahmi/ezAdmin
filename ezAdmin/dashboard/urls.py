from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexTemplateView.as_view(), name = 'dashboard-index'),
    path('guideline', DocumentationView.as_view(), name = 'dashboard-documentation'),
    path('dashboard/update-dark-mode/', UpdateDarkModeView.as_view(), name='dashboard-update-dark-mode'),
]