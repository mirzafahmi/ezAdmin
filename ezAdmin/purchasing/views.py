from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from mixins.validation_mixin import QuantityValidationMixin
from collections import Counter
import re

from .models import *
from .forms import *

import csv
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import sys


class PurchasingMainView(LoginRequiredMixin, TemplateView):
    template_name = 'purchasing/purchasing_main.html'

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'purchasing/supplier_list.html'
    context_object_name = 'suppliers'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return Supplier.objects.all()

class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_create.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    permission_required = 'purchasing.add_supplier'

    def form_valid(self, form):
        supplier_name = form.cleaned_data['company_name']
        messages.success(self.request, f'{supplier_name} supplier account created successfully!')

        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_update.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    permission_required = 'purchasing.change_supplier'

    def form_valid(self, form):
        supplier_name = self.get_object().company_name
        messages.success(self.request, f'{supplier_name} supplier account updated successfully!')

        return super().form_valid(form)

class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'purchasing/supplier_delete.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    permission_required = 'purchasing.delete_supplier'
    
    def post(self, request, *args, **kwargs):
        supplier_name = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{supplier_name} supplier deleted successfully!'
            messages.success(self.request, success_message)

        return response

class PurchasingDocumentListView(LoginRequiredMixin, ListView):
    model = PurchasingDocument
    template_name = 'purchasing/purchasing_document_list.html'
    context_object_name = 'purchasing_documents'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return PurchasingDocument.objects.all()

class PurchasingDocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PurchasingDocument
    form_class = PurchasingDocumentForm
    template_name = 'purchasing/purchasing_document_create.html'
    success_url = reverse_lazy('purchasing-purchasing-document-list')

    permission_required = 'purchasing.add_purchasingdocument'

    def form_valid(self, form):
        po_number = form.cleaned_data['po_number']
        messages.success(self.request, f'{po_number} purchasing document created successfully!')

        return super().form_valid(form)

class PurchasingDocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PurchasingDocument
    form_class = PurchasingDocumentForm
    template_name = 'purchasing/purchasing_document_update.html'
    success_url = reverse_lazy('purchasing-purchasing-document-list')
    context_object_name = 'purchasing_document'

    permission_required = 'purchasing.change_purchasingdocument'

    def form_valid(self, form):
        purchasing_document = form.save(commit=False)  # Get the object from the form
        
        messages.success(self.request, f'{purchasing_document.po_number} purchasing document updated successfully!')

        return super().form_valid(form)
    

class PurchasingDocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PurchasingDocument
    template_name = 'purchasing/purchasing_document_delete.html'
    context_object_name = 'purchasing_document'
    success_url = reverse_lazy('purchasing-purchasing-document-list')

    permission_required = 'purchasing.delete_purchasingdocument'

    def post(self, request, *args, **kwargs):
        purchasing_document = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{purchasing_document} purchasing document deleted successfully!'
            messages.success(self.request, success_message)

        return response
