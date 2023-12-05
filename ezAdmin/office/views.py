from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.http import JsonResponse

from .models import *
from .forms import *

class OfficeMainView(LoginRequiredMixin, TemplateView):
    template_name = 'office/office_main.html'

class ElectronicUserLocationListView(LoginRequiredMixin, ListView):
    model = ElectronicUserLocation
    template_name = 'office/electronic_user_location_list.html'
    context_object_name = 'electronicuserlocations'  # The variable name in the template

class ElectronicUserLocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicUserLocation
    form_class = ElectronicUserLocationForm
    template_name = 'office/electronic_user_location_create.html'
    success_url = reverse_lazy('office-electronic-user-location-list')

    permission_required = 'office.add_electronicuserlocation'

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        cleaned_phone_number = ''.join(filter(str.isdigit, str(phone_number)))
        
        formatted_phone_number = f"+{cleaned_phone_number[0:2]} {cleaned_phone_number[2:4]}-{cleaned_phone_number[4:7]} {cleaned_phone_number[7:]}"

        return formatted_phone_number

    def form_valid(self, form):
        company_name = form.cleaned_data['company_name']
        careholder_name = form.cleaned_data['careholder_name']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{company_name} ({careholder_name}) electronic user location created successfully!')

        return super().form_valid(form)

class ElectronicUserLocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicUserLocation
    form_class = ElectronicUserLocationForm
    template_name = 'office/electronic_user_location_update.html'
    success_url = reverse_lazy('office-electronic-user-location-list')

    permission_required = 'office.change_electronicuserlocation'

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        cleaned_phone_number = ''.join(filter(str.isdigit, str(phone_number)))
        
        formatted_phone_number = f"+{cleaned_phone_number[0:2]} {cleaned_phone_number[2:4]}-{cleaned_phone_number[4:7]} {cleaned_phone_number[7:]}"

        return formatted_phone_number

    def form_valid(self, form):
        company_name = self.get_object()

        messages.success(self.request, f'{company_name} ({company_name.careholder_name}) electronic user location updated successfully!')

        return super().form_valid(form)

class ElectronicUserLocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicUserLocation
    template_name = 'office/electronic_user_location_delete.html'
    success_url = reverse_lazy('office-electronic-user-location-list')

    permission_required = 'office.delete_electronicuserlocation'
    
    def post(self, request, *args, **kwargs):
        company_name = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{company_name} ({company_name.careholder_name}) electronic user location deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicUserListView(LoginRequiredMixin, ListView):
    model = ElectronicUser
    template_name = 'office/electronic_user_list.html'
    context_object_name = 'electronicusers' 

class ElectronicUserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicUser
    form_class = ElectronicUserForm
    template_name = 'office/electronic_user_create.html'
    success_url = reverse_lazy('office-electronic-user-list')

    permission_required = 'office.add_electronicuser'

    def form_valid(self, form):
        user_name = form.cleaned_data['name']
        user_position = form.cleaned_data['position']
        user_location = form.cleaned_data['location']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{user_name} ({user_position}) electronic user from {user_location} created successfully!')

        return super().form_valid(form)

class ElectronicUserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicUser
    form_class = ElectronicUserForm
    template_name = 'office/electronic_user_update.html'
    success_url = reverse_lazy('office-electronic-user-list')

    permission_required = 'office.change_electronicuser'

    def form_valid(self, form):
        user = self.get_object()

        messages.success(self.request, f'{user.name} ({user.position}) electronic user from {user.location} updated successfully!')

        return super().form_valid(form)

class ElectronicUserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicUser
    template_name = 'office/electronic_user_delete.html'
    success_url = reverse_lazy('office-electronic-user-list')

    permission_required = 'office.delete_electronicuser'
    
    def post(self, request, *args, **kwargs):
        user_name = self.get_object()
        location = self.get_object().location

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{user.name} ({user.position}) electronic user from {user.location} deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicBrandListView(LoginRequiredMixin, ListView):
    model = ElectronicBrand
    template_name = 'office/electronic_brand_list.html'
    context_object_name = 'electronicbrands' 

class ElectronicBrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicBrand
    form_class = ElectronicBrandForm
    template_name = 'office/electronic_brand_create.html'
    success_url = reverse_lazy('office-electronic-brand-list')

    permission_required = 'office.add_electronicbrand'

    def form_valid(self, form):
        brand_name = form.cleaned_data['brand_name']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{brand_name} electronic brand created successfully!')

        return super().form_valid(form)

class ElectronicBrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicBrand
    form_class = ElectronicBrandForm
    template_name = 'office/electronic_brand_update.html'
    success_url = reverse_lazy('office-electronic-brand-list')

    permission_required = 'office.change_electronicbrand'

    def form_valid(self, form):
        brand_name = self.get_object()

        messages.success(self.request, f'{brand_name} electronic brand updated successfully!')

        return super().form_valid(form)

class ElectronicBrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicBrand
    template_name = 'office/electronic_brand_delete.html'
    success_url = reverse_lazy('office-electronic-brand-list')

    permission_required = 'office.delete_electronicbrand'
    
    def post(self, request, *args, **kwargs):
        brand_name = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{brand_name} electronic brand deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicModelListView(LoginRequiredMixin, ListView):
    model = ElectronicModel
    template_name = 'office/electronic_model_list.html'
    context_object_name = 'electronicmodels' 

class ElectronicModelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicModel
    form_class = ElectronicModelForm
    template_name = 'office/electronic_model_create.html'
    success_url = reverse_lazy('office-electronic-model-list')

    permission_required = 'office.add_electronicmodel'

    def form_valid(self, form):
        brand = form.cleaned_data['brand']
        model_name = form.cleaned_data['model_name']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{brand} ({model_name}) electronic model created successfully!')

        return super().form_valid(form)

class ElectronicModelUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicModel
    form_class = ElectronicModelForm
    template_name = 'office/electronic_model_update.html'
    success_url = reverse_lazy('office-electronic-model-list')

    permission_required = 'office.change_electronicmodel'

    def form_valid(self, form):
        model = self.get_object()

        messages.success(self.request, f'{model.model_name} electronic model for brand {model.brand} updated successfully!')

        return super().form_valid(form)

class ElectronicModelDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicModel
    template_name = 'office/electronic_model_delete.html'
    success_url = reverse_lazy('office-electronic-model-list')

    permission_required = 'office.delete_electronicmodel'
    
    def post(self, request, *args, **kwargs):
        model = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{model} electronic model for brand {model.brand} deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicPurchasingDocumentListView(LoginRequiredMixin, ListView):
    model = ElectronicPurchasingDocument
    template_name = 'office/electronic_purchasing_document_list.html'
    context_object_name = 'electronicpurchasingdocuments' 

class ElectronicPurchasingDocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicPurchasingDocument
    form_class = ElectronicPurchasingDocumentForm
    template_name = 'office/electronic_purchasing_document_create.html'
    success_url = reverse_lazy('office-electronic-purchasing-document-list')

    permission_required = 'office.add_electronicpurchasingdocument'

    def form_valid(self, form):
        po_number = form.cleaned_data['po_number']
        supplier = form.cleaned_data['supplier']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{po_number} ({supplier}) electronic purchasing document created successfully!')

        return super().form_valid(form)

class ElectronicPurchasingDocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicPurchasingDocument
    form_class = ElectronicPurchasingDocumentForm
    template_name = 'office/electronic_purchasing_document_update.html'
    success_url = reverse_lazy('office-electronic-purchasing-document-list')

    permission_required = 'office.change_electronicpurchasingdocument'

    def form_valid(self, form):
        po_number = self.get_object()

        messages.success(self.request, f'{po_number} ({po_number.supplier}) electronic purchasing document updated successfully!')

        return super().form_valid(form)

class ElectronicPurchasingDocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicPurchasingDocument
    template_name = 'office/electronic_purchasing_document_delete.html'
    success_url = reverse_lazy('office-electronic-purchasing-document-list')

    permission_required = 'office.delete_electronicpurchasingdocument'
    
    def post(self, request, *args, **kwargs):
        po_number = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{po_number} ({po_number.supplier}) electronic purchasing document deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicInventoryListView(LoginRequiredMixin, ListView):
    model = ElectronicInventory
    template_name = 'office/electronic_inventory_list.html'
    context_object_name = 'electronicinventories' 

class ElectronicInventoryListViewAJAX(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        purchasing_doc = request.GET.get('purchasing_doc')

        response_data = []

        if purchasing_doc:

            purchasing_doc_details = ElectronicPurchasingDocument.objects.filter(id=purchasing_doc).first()

            response_data.append({
                'supplier': purchasing_doc_details.supplier.company_name,
                'po_number': purchasing_doc_details.po_number,
                'po_doc': str(purchasing_doc_details.po_doc),
                'invoice_number': purchasing_doc_details.invoice_number,
                'invoice_doc': str(purchasing_doc_details.invoice_doc),
                'create_date': purchasing_doc_details.create_date,
            })

        return JsonResponse(response_data, safe=False)

class ElectronicInventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicInventory
    form_class = ElectronicInventoryForm
    template_name = 'office/electronic_inventory_create.html'
    success_url = reverse_lazy('office-electronic-inventory-list')

    permission_required = 'office.add_electronicinventory'

    def form_valid(self, form):
        electronic_item = form.cleaned_data['electronic_item']
        serial_number = form.cleaned_data['serial_number']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{electronic_item} ({serial_number}) electronic inventory created successfully!')

        return super().form_valid(form)

class ElectronicInventoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicInventory
    form_class = ElectronicInventoryForm
    template_name = 'office/electronic_inventory_update.html'
    success_url = reverse_lazy('office-electronic-inventory-list')

    permission_required = 'office.change_electronicinventory'

    def form_valid(self, form):
        inventory = self.get_object()

        messages.success(self.request, f'{inventory.electronic_item} ({inventory.serial_number}) electronic inventory updated successfully!')

        return super().form_valid(form)

class ElectronicInventoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicInventory
    template_name = 'office/electronic_purchasing_document_delete.html'
    success_url = reverse_lazy('office-electronic-inventory-list')

    permission_required = 'office.delete_electronicinventory'
    
    def post(self, request, *args, **kwargs):
        inventory = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{inventory.electronic_item} ({electronic_item.serial_number}) electronic inventory deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ElectronicTransactionListView(LoginRequiredMixin, ListView):
    model = ElectronicTransaction
    template_name = 'office/electronic_transaction_list.html'
    context_object_name = 'electronictransactions' 

class ElectronicTransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ElectronicTransaction
    form_class = ElectronicTransactionForm
    template_name = 'office/electronic_transaction_create.html'
    success_url = reverse_lazy('office-electronic-transaction-list')

    permission_required = 'office.add_electronictransaction'

    def form_valid(self, form):
        electronic_item = form.cleaned_data['electronic_item']
        current_user = form.cleaned_data['current_user']

        form.instance.create_by = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, f'{current_user} ({electronic_item} | {electronic_item.serial_number}) transaction created successfully!')

        return super().form_valid(form)

class ElectronicTransactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ElectronicTransaction
    form_class = ElectronicTransactionForm
    template_name = 'office/electronic_transaction_update.html'
    success_url = reverse_lazy('office-electronic-transaction-list')

    permission_required = 'office.change_electronictransaction'

    def form_valid(self, form):
        transaction = self.get_object()

        messages.success(self.request, f'{transaction.current_user} {transaction.electronic_item.electronic_item.brand.brand_name} {transaction.electronic_item.electronic_item.model_name} (SN: {transaction.electronic_item.serial_number}) transaction updated successfully!')

        return super().form_valid(form)

class ElectronicTransactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ElectronicTransaction
    template_name = 'office/electronic_transaction_delete.html'
    success_url = reverse_lazy('office-electronic-transaction-list')

    permission_required = 'office.delete_electronictransaction'
    
    def post(self, request, *args, **kwargs):
        transaction= self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{transaction.current_user} {transaction.electronic_item.electronic_item.brand.brand_name} {transaction.electronic_item.electronic_item.model_name} (SN: {transaction.electronic_item.serial_number}) transaction deleted successfully!'
            messages.success(self.request, success_message)

        return response