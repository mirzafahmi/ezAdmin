from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib import messages

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'purchasing/supplier_list.html'
    context_object_name = 'suppliers'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return Supplier.objects.all()

class SupplierCreateView(LoginRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_create.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def form_valid(self, form):
        supplier_name = form.cleaned_data['company_name']
        messages.success(self.request, f'{supplier_name} created successfully!')

        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_update.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def form_valid(self, form):
        supplier_name = self.get_object().company_name
        messages.success(self.request, f'{supplier_name} updated successfully!')

        return super().form_valid(form)

class SupplierDeleteView(LoginRequiredMixin,DeleteView):
    model = Supplier
    template_name = 'purchasing/supplier_delete.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def delete(self, request, *args, **kwargs):
        supplier_name = self.get_object().company_name
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{supplier_name} deleted successfully!')

        return response

class PurchasingDocumentListView(LoginRequiredMixin, ListView):
    model = PurchasingDocument
    template_name = 'purchasing/purchasing_document_list.html'
    context_object_name = 'purchasing_documents'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return PurchasingDocument.objects.all()

class PurchasingDocumentCreateView(LoginRequiredMixin,CreateView):
    model = PurchasingDocument
    form_class = PurchasingDocumentForm
    template_name = 'purchasing/purchasing_document_create.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def form_valid(self, form):
        po_number = form.cleaned_data['po_number']
        messages.success(self.request, f'{po_number} created successfully!')

        return super().form_valid(form)

class PurchasingDocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchasingDocument
    form_class = PurchasingDocumentForm
    template_name = 'purchasing/purchasing_document_update.html'
    success_url = reverse_lazy('purchasing-supplier-list')
    context_object_name = 'purchasing_document'

    def form_valid(self, form):
        purchasing_document = self.get_object().po_number
        messages.success(self.request, f'{purchasing_document} updated successfully!')

        return super().form_valid(form)


class PurchasingDocumentDeleteView(LoginRequiredMixin,DeleteView):
    model = PurchasingDocument
    template_name = 'purchasing/purchasing_document_delete.html'
    context_object_name = 'purchasing_document'
    success_url = reverse_lazy('purchasing-purchasing-document-list')

    def delete(self, request, *args, **kwargs):
        purchasing_document = self.get_object().company_name
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{purchasing_document} deleted successfully!')

        return response

class RawMaterialIdentifierCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialIdentifier
    form_class = RawMaterialIdentifierForm
    template_name = 'purchasing/raw_material_identifier_create.html'
    success_url = reverse_lazy('purchasing-raw-material-identifier-list')

    def form_valid(self, form):
        identifier = form.cleaned_data['parent_item_code']
        messages.success(self.request, f'{identifier} created successfully!')

        return super().form_valid(form)

class RawMaterialIdentifierListView(LoginRequiredMixin, ListView):
    model = RawMaterialIdentifier
    template_name = 'purchasing/raw_material_identifier_list.html'
    context_object_name = 'identifiers'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialIdentifier.objects.all()

class RawMaterialIdentifierUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialIdentifier
    form_class = RawMaterialIdentifierForm
    template_name = 'purchasing/raw_material_identifier_update.html'
    success_url = reverse_lazy('purchasing-raw-material-identifier-list')
    context_object_name = 'identifier'

    def form_valid(self, form):
        identifier = self.get_object().parent_item_code
        messages.success(self.request, f'{identifier} updated successfully!')

        return super().form_valid(form)


class RawMaterialIdentifierDeleteView(LoginRequiredMixin,DeleteView):
    model = RawMaterialIdentifier
    template_name = 'purchasing/raw_material_identifier_delete.html'
    context_object_name = 'identifier'
    success_url = reverse_lazy('purchasing-raw-material-identifier-list')

    def delete(self, request, *args, **kwargs):
        identifier = self.get_object().parent_item_code
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{identifier} deleted successfully!')

        return response