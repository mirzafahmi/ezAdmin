from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Supplier
from .forms import SupplierForm

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_create.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def form_valid(self, form):
        # Customize the form validation or save logic if needed
        return super().form_valid(form)

class SupplierListView(ListView):
    model = Supplier
    template_name = 'purchasing/supplier_list.html'
    context_object_name = 'suppliers'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):
        return Supplier.objects.all()