from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from .models import *
from django.urls import reverse_lazy, reverse

class MiscMainView(LoginRequiredMixin, TemplateView):
    template_name = 'misc/misc_main.html'

# Create your views here.
class UOMListView(LoginRequiredMixin, ListView):
    model = UOM
    template_name = 'misc/UOM_list.html'
    context_object_name = 'UOMs'

    def get_queryset(self):

        return UOM.objects.all()

class UOMCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UOM
    form_class = UOMForm
    template_name = 'misc/UOM_create.html'
    success_url = reverse_lazy('misc-uom-list')

    permission_required = 'misc.add_uom'

    def form_valid(self, form):
        uom_name = form.cleaned_data['name']

        messages.success(self.request, f'{uom_name} UOM created successfully!')

        return super().form_valid(form)
    
class UOMUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UOM
    form_class = UOMForm
    template_name = 'misc/UOM_update.html'
    success_url = reverse_lazy('misc-uom-list')
    context_object_name = 'UOM'

    permission_required = 'misc.change_uom'

    def form_valid(self, form):
        uom_name = self.get_object().name
        
        messages.success(self.request, f'{uom_name} UOM updated successfully!')

        return super().form_valid(form)
    
class UOMDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = UOM
    template_name = 'misc/UOM_delete.html'
    success_url = reverse_lazy('misc-uom-list')
    context_object_name = 'UOM'

    permission_required = 'misc.delete_uom'
    
    def post(self, request, *args, **kwargs):
        uom_name = self.get_object()
        success_message = f'{uom_name} UOM deleted successfully!'

        messages.success(self.request, success_message)

        return super().post(request, *args, **kwargs)

class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = 'misc/currency_list.html'
    context_object_name = 'currencies'

class CurrencyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'misc/currency_create.html'
    success_url = reverse_lazy('misc-currency-list')

    permission_required = 'misc.add_currency'

    def form_valid(self, form):
        currency = form.cleaned_data['name']
        currency_code = form.cleaned_data['currency_code']

        messages.success(self.request, f'{currency}({currency_code}) currency created successfully!')

        return super().form_valid(form)

class CurrencyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'misc/currency_update.html'
    success_url = reverse_lazy('misc-currency-list')
    context_object_name = 'currency'

    permission_required = 'misc.change_currency'

    def form_valid(self, form):
        currency = self.get_object()

        messages.success(self.request, f'{currency.name}({currency.currency_code}) currency updated successfully!')

        return super().form_valid(form)

class CurrencyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Currency
    template_name = 'misc/currency_delete.html'
    success_url = reverse_lazy('misc-currency-list')
    context_object_name = 'currency'

    permission_required = 'misc.delete_currency'
    
    def post(self, request, *args, **kwargs):
        currency = self.get_object()
        success_message = f'{currency.name}({currency.currency_code}) currency deleted successfully!'
        messages.success(self.request, success_message)

        return super().post(request, *args, **kwargs)
    
