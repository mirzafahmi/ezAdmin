from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from mixins.validation_mixin import QuantityValidationMixin
from collections import Counter
import re

class PurchasingMainView(LoginRequiredMixin, TemplateView):
    template_name = 'purchasing/purchasing_main.html'

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
        messages.success(self.request, f'{supplier_name} account created successfully!')

        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchasing/supplier_update.html'
    success_url = reverse_lazy('purchasing-supplier-list')

    def form_valid(self, form):
        supplier_name = self.get_object().company_name
        messages.success(self.request, f'{supplier_name} account updated successfully!')

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
    success_url = reverse_lazy('purchasing-purchasing-document-list')

    def form_valid(self, form):
        po_number = form.cleaned_data['po_number']
        messages.success(self.request, f'{po_number} created successfully!')

        return super().form_valid(form)

class PurchasingDocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchasingDocument
    form_class = PurchasingDocumentForm
    template_name = 'purchasing/purchasing_document_update.html'
    success_url = reverse_lazy('purchasing-purchasing-document-list')
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

    def get_success_url(self):
        if 'identifier_create' in self.request.get_full_path():
            return reverse('purchasing-raw-material-inventory-identifier-based-list')
        else:
            return reverse('purchasing-raw-material-identifier-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['cancel_url'] = self.get_success_url()  # Use the success URL as cancel URL for simplicity
        
        return context

    def form_valid(self, form):
        identifier = form.cleaned_data['parent_item_code'].upper()
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

class RawMaterialComponentCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialComponent
    form_class = RawMaterialComponentForm
    template_name = 'purchasing/raw_material_component_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'identifier_id' in self.kwargs:
            kwargs['initial']['identifier_id'] = self.kwargs.get('identifier_id')

        return kwargs

    def get_success_url(self):
        # Check if the identifier_id is in the URL
        if 'identifier_id' in self.kwargs:
            identifier_id = self.kwargs['identifier_id']  # Get the 'identifier_name' parameter
            # Construct the success URL with the 'identifier_name'
            return reverse('purchasing-raw-material-inventory-identifier-component-based-list', kwargs={'identifier_id': identifier_id})
        else:
            return reverse_lazy('purchasing-raw-material-component-list')
    
    def get_cancel_url(self):
        if 'identifier_id' in self.kwargs:
            identifier_id = self.kwargs['identifier_id']  # Get the 'identifier_name' parameter
            # Construct the success URL with the 'identifier_name'
            return reverse('purchasing-raw-material-inventory-identifier-component-based-list', kwargs={'identifier_id': identifier_id})
        else:
            return reverse_lazy('purchasing-raw-material-component-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.get_cancel_url()
        return context

    def form_valid(self, form):
        component = form.cleaned_data['component']
        messages.success(self.request, f'{component} for {form.cleaned_data["identifier"]} created successfully!')

        return super().form_valid(form)

class RawMaterialComponentListView(LoginRequiredMixin, ListView):
    model = RawMaterialComponent
    template_name = 'purchasing/raw_material_component_list.html'
    #context_object_name = 'components'  # The variable name in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        components = RawMaterialComponent.objects.all()

        component = RawMaterialComponent.objects.values_list('component', flat=True)

        # Extract words and phrases (splitting on commas)
        all_words = ','.join(component)
        all_words_list = all_words.split(',')
        
        simple_words = set() #store only distint data

        for word in all_words_list:
            if 'for' not in word.lower():  # Exclude words with 'for'
                simple_words.add(word)

        context['components'] = components
        context['unique_components'] = simple_words

        return context

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialComponent.objects.all()

class RawMaterialComponentListViewAJAX(View):
    def get(self, request, *args, **kwargs):
        component_name = request.GET.get('component_name')
        print(component_name)
        filter_data =[]

        if component_name:
            # Filter the model objects based on the component name
            filtered_objects = RawMaterialComponent.objects.filter(component__icontains=component_name)

            filter_components = filtered_objects
            print(filter_components)
            for filter_component in filter_components:
                filter_data.append({
                    'identifier': filter_component.identifier.parent_item_code,
                    'identifier_id': filter_component.identifier_id,
                    'component': filter_component.component,
                    'component_id': filter_component.id,
                    'specifications': filter_component.spec,
                    'create_date': filter_component.create_date,
                })

            
            return JsonResponse(filter_data, safe=False)
        else:
            return JsonResponse({'error': 'No component name provided'}, status=400)

        '''if identifier_id:
            filter_logs = RawMaterialComponent.objects.filter(component=component_id)
            
            for filter_log in filter_logs:
                filter_data.append({
                    'identifier': identifiers_based.identifier,
                    'identifier_id': identifiers_based.identifier.parent_item_code,
                    'component': identifiers_based.component,
                    'component_id': identifiers_based.id,
                    'specifications': identifiers_based.spec,
                    'create_date': identifiers_based.id,
                })
        else:
            filter_names = RawMaterialComponent.objects.all()

            for filter_name in filter_names:
                #print(filter_name.component)
                filter_data.append({
                    'identifier': filter_name.identifier.parent_item_code,
                    'identifier_id': filter_name.identifier.parent_item_code,
                    'component': filter_name.component,
                    'component_id': filter_name.id,
                    'specifications': filter_name.spec,
                    'create_date': filter_name.id,
                })'''


        #return JsonResponse(filter_data, safe=False)


class RawMaterialComponentUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialComponent
    form_class = RawMaterialComponentForm
    template_name = 'purchasing/raw_material_component_update.html'
    success_url = reverse_lazy('purchasing-raw-material-component-list')
    context_object_name = 'component'

    def form_valid(self, form):
        component = self.get_object()
        messages.success(self.request, f'{component.component} for {component.identifier} updated successfully!')

        return super().form_valid(form)

class RawMaterialComponentDeleteView(LoginRequiredMixin,DeleteView):
    model = RawMaterialComponent
    template_name = 'purchasing/raw_material_component_delete.html'
    context_object_name = 'component'
    success_url = reverse_lazy('purchasing-raw-material-component-list')

    def delete(self, request, *args, **kwargs):
        component = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{component.component} for {component.identifier} deleted successfully!')

        return response

class BOMComponentCreateView(LoginRequiredMixin,CreateView):
    model = BOMComponent
    form_class = BOMComponentForm
    template_name = 'purchasing/BOM_component_create.html'
    success_url = reverse_lazy('purchasing-BOM-component-list')

    def form_valid(self, form):
        BOMcomponent = form.cleaned_data['product']
        messages.success(self.request, f'{BOMcomponent} for {form.cleaned_data["product"]} created successfully!')

        return super().form_valid(form)

class BOMComponentListView(LoginRequiredMixin, ListView):
    model = BOMComponent
    template_name = 'purchasing/BOM_component_list.html'
    context_object_name = 'BOMcomponents'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return BOMComponent.objects.all()

class BOMComponentUpdateView(LoginRequiredMixin, UpdateView):
    model = BOMComponent
    form_class = BOMComponentForm
    template_name = 'purchasing/BOM_component_update.html'
    success_url = reverse_lazy('purchasing-BOM-component-list')
    context_object_name = 'BOMcomponent'

    def form_valid(self, form):
        BOMcomponent = self.get_object()
        messages.success(self.request, f'{BOMcomponent.raw_material_component} updated successfully!')

        return super().form_valid(form)


class BOMComponentDeleteView(LoginRequiredMixin,DeleteView):
    model = BOMComponent
    template_name = 'purchasing/BOM_component_delete.html'
    context_object_name = 'BOMcomponent'
    success_url = reverse_lazy('purchasing-BOM-component-list')

    def delete(self, request, *args, **kwargs):
        BOMcomponent = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{BOMcomponent.raw_material_component} deleted successfully!')

        return response

class RawMaterialInventoryLogMainView(LoginRequiredMixin, TemplateView):
    template_name = 'purchasing/raw_material_inventory_log_main.html'

class InventoryMainView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/inventory_main.html'

class RawMaterialMainView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/raw_material_main.html'

class RawMaterialInventoryCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_create.html'
    success_url = reverse_lazy('purchasing-raw-material-inventory-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['initial']['identifier_id'] = self.kwargs.get('identifier_id')
        kwargs['initial']['stock_type'] = self.kwargs.get('stock_type', '1')  # Default to stock-in

        return kwargs

    def form_valid(self, form):
        RawMaterialInventory = form.cleaned_data
        print(RawMaterialInventory)
        messages.success(self.request, f'{RawMaterialInventory["component"]} log of {RawMaterialInventory["purchasing_doc"]} created successfully!')

        return super().form_valid(form)

class RawMaterialInventoryAJAX(View):
    def get(self, request, *args, **kwargs):
        identifier_id = request.GET.get('identifier_id')
        component_id = request.GET.get('component_id')
        stock_type = request.GET.get('type')

        if stock_type == '2':
            raw_material = RawMaterialInventory.objects.filter(
                component_id=component_id,
                stock_type='1',  # Stock In
            ).extra(
                select={'formatted_date': "(exp_date || '-01')"}
            ).order_by('formatted_date').first()

            if raw_material:
                    fifo_info = {
                        'component': raw_material.component.id,
                        'lot_number': raw_material.lot_number,
                        'exp_date': raw_material.exp_date,
                        'price_per_unit': raw_material.price_per_unit,
                        'purchasing_doc': raw_material.purchasing_doc_id,  # Assuming purchasing_doc is a ForeignKey
                    }

                    return JsonResponse(fifo_info)
        else:
            fifo_info = {
                'component': component_id
            }
        #create else for the type 1 to handle the value
        return JsonResponse(fifo_info)

class RawMaterialInventoryListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_list.html'
    context_object_name = 'RawMaterialInventories'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialInventory.objects.all()

class RawMaterialInventoryIdentifierBasedListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_based_main.html'
    context_object_name = 'RawMaterialInventoriesIdentifierBaseds'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):
        # Use select_related to fetch the related RawMaterialComponent and RawMaterialIdentifier
        queryset = RawMaterialIdentifier.objects.values_list('parent_item_code', 'id').distinct()

        return queryset

class RawMaterialInventoryIdentifierComponentBasedListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        identifier = get_object_or_404(RawMaterialIdentifier, id=identifier_id)

        queryset = RawMaterialComponent.objects.filter(identifier=identifier)
        
        # Extracting a list of distinct components and their IDs
        distinct_components = queryset.values_list('component', flat=True).distinct()
        distinct_components_ids = queryset.values_list('id', flat=True).distinct()
        print(queryset)
        print(queryset.exists())
        # Creating a list of dictionaries for components with their ID and name
        components_list = [{'id': component_id, 'name': component_name} for component_id, component_name in zip(distinct_components_ids, distinct_components)]

        # Adding the extracted data to the context
        context['raw_material_inventory_list_identifier_component_baseds'] = components_list
        context['parent_item_code'] = identifier
        context['identifier_id'] = identifier_id
        context['exists_flag'] = queryset.exists()

        return context

class RawMaterialInventoryIdentifierComponentBasedLogCreateMainView(LoginRequiredMixin, TemplateView, QuantityValidationMixin):
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_log_create_main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        component_id = self.kwargs.get('component_id')

        queryset = RawMaterialInventory.objects.filter(component__id=component_id)

        distinct_components = queryset.values_list('component__component').distinct()

        context['RawMaterialInventoriesIdentifierComponentBasedLogs'] = queryset
        context['identifier_id'] = identifier_id
        context['component_id'] = component_id
        context['component'] = queryset.values_list('component__identifier__parent_item_code', 'component__component').distinct()

        return context
    
class RawMaterialInventoryIdentifierComponentBasedLogCreateView(LoginRequiredMixin, CreateView, QuantityValidationMixin):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_log_create.html'

    def get_success_url(self):
        identifier_id = self.kwargs.get('identifier_id')
        component_id = self.kwargs.get('component_id')
        stock_type = self.kwargs.get('stock_type', '1')

        return reverse_lazy('purchasing-raw-material-inventory-identifier-component-based-log-list', args=[identifier_id, component_id])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['identifier_id'] = self.kwargs.get('identifier_id')
        kwargs['initial']['component_id'] = self.kwargs.get('component_id')
        kwargs['initial']['stock_type'] = self.kwargs.get('stock_type', '1')  # Default to stock-in

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        component_id = self.kwargs.get('component_id')
        stock_type = self.kwargs.get('stock_type', '1')

        identifier_name = RawMaterialIdentifier.objects.get(id = identifier_id)
        component_name = RawMaterialComponent.objects.get(id = component_id)

        context['identifier_id'] = identifier_id
        context['component_id'] = component_id
        context['stock_type'] = stock_type

        context['identifier_name'] = identifier_name
        context['component_name'] = component_name

        return context

    def form_valid(self, form):
        raw_material_inventory = form.save(commit=False)

        component = raw_material_inventory.component
        purchasing_doc = raw_material_inventory.purchasing_doc

        raw_material_inventory.save()

        messages.success(self.request, f'{component} log of {purchasing_doc} created successfully!')

        return super().form_valid(form)

class RawMaterialInventoryIdentifierComponentBasedLogCreateAJAX(View, QuantityValidationMixin):
    def get(self, request, *args, **kwargs):
        identifier_id = request.GET.get('identifier_id')
        component_id = request.GET.get('component_id')
        stock_type = request.GET.get('type')
        quantity = int(request.GET.get('quantity', 0))

        response_data = {
            'component': component_id,
            'available_quantity': None,
            'alert': False,
            'related_stock_in': None,
        }

        if stock_type == '2':
            current_raw_material, current_raw_material_quantity = self.get_available_quantity(component_id)
            print(current_raw_material)
            #print(current_raw_material.stock_in_tag.id)
            if current_raw_material_quantity is not None:
                response_data = {
                    'component': current_raw_material.component.id,
                    'lot_number': current_raw_material.lot_number,
                    'exp_date': current_raw_material.exp_date,
                    'price_per_unit': current_raw_material.price_per_unit,
                    'purchasing_doc': current_raw_material.purchasing_doc_id,
                    'available_quantity': current_raw_material_quantity,
                    'stock_in_tag': current_raw_material.stock_in_tag.id,
                }
            else:
                response_data = {
                    'component': component_id, 
                    'available_quantity': 0, 
                    }

        if stock_type == None:
            current_raw_material, current_raw_material_quantity = self.get_available_quantity(component_id)
            component = RawMaterialComponent.objects.get(id=component_id)
            print(current_raw_material_quantity)
            if current_raw_material is None:
                response_data = {
                        'component': component_id,
                        'component_name': component.component, 
                        'identifier_name': component.identifier.parent_item_code, 
                        'available_quantity': 'Empty', 
                        'alert': True
                    }
            else:
                response_data = {
                        'component': component_id,
                        'component': RawMaterialComponent.objects.get(id = component_id).component, 
                        'available_quantity': 'Empty', 
                        'alert': False
                    }

        return JsonResponse(response_data)

class RawMaterialInventoryIdentifierComponentBasedLogListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_log_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        component_id = self.kwargs.get('component_id')

        queryset = RawMaterialInventory.objects.filter(component__id=component_id)

        distinct_components = queryset.values_list('component__component').distinct()

        stock_in_items = RawMaterialInventory.objects.filter(
            component_id=component_id,
            stock_type='1',
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        stock_out_items = RawMaterialInventory.objects.filter(
            component_id=component_id,
            stock_type='2',
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        balance_quantity_component_based = stock_in_items - stock_out_items

        context['RawMaterialInventoriesIdentifierComponentBasedLogs'] = queryset
        context['exists_flag'] = queryset.exists()
        context['identifier_id'] = identifier_id
        context['component_id'] = component_id
        context['component'] = queryset.values_list('component__identifier__parent_item_code', 'component__component').distinct()
        context['balance'] = balance_quantity_component_based

        return context

class RawMaterialInventoryIdentifierComponentBasedLogListViewAJAX(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        identifier_id = request.GET.get('identifier_id')
        component_id = request.GET.get('component_id')
        stock_in_tag = request.GET.get('stock_in_tag') 
        purchasing_doc = request.GET.get('purchasing_doc')

        stock_in_items = RawMaterialInventory.objects.filter(
            component_id=component_id,
            stock_type='1',
        ).order_by('exp_date')

        response_data = []

        if stock_in_tag:
            # If stock_in_tag is provided, filter based on it
            stock_tag_baseds = RawMaterialInventory.objects.filter(
                stock_in_tag=stock_in_tag
            )

            stock_in_tag_based = RawMaterialInventory.objects.filter(
                stock_in_tag=stock_in_tag,
                stock_type='1',
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            stock_out_tag_based = RawMaterialInventory.objects.filter(
                stock_in_tag=stock_in_tag,
                stock_type='2',
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            balance_quantity_tag_based = stock_in_tag_based - stock_out_tag_based

            #get data for purchasing doc
            print(stock_tag_baseds)
            for stock_tag_based in stock_tag_baseds:
                response_data.append({
                    'log_id': stock_tag_based.id,
                    'identifier': stock_tag_based.component.identifier.parent_item_code,
                    'identifier_id': stock_tag_based.component.identifier.id,
                    'component': stock_tag_based.component.component,
                    'component_id': stock_tag_based.component.id,
                    'quantity': stock_tag_based.quantity,
                    'lot': stock_tag_based.lot_number,
                    'expiry_date': stock_tag_based.exp_date,
                    'stock_in_date': stock_tag_based.stock_in_date,
                    'stock_out_date': stock_tag_based.stock_out_date,
                    'price_per_unit': stock_tag_based.price_per_unit,
                    'purchasing_document': stock_tag_based.purchasing_doc.po_number,
                    'purchasing_document_id': stock_tag_based.purchasing_doc.id,
                    'company_name': stock_tag_based.purchasing_doc.supplier.company_name,
                    'stock_in_tag': stock_tag_based.stock_in_tag.id,
                    'stock_type': stock_tag_based.stock_type,
                    'balance': balance_quantity_tag_based,
                })
        elif purchasing_doc:
            purchasing_doc_details = PurchasingDocument.objects.filter(id=purchasing_doc).first()
            print(purchasing_doc_details.AWB_doc)
            print(purchasing_doc_details.po_doc)
            response_data.append({
                'supplier': purchasing_doc_details.supplier.company_name,
                'po_number': purchasing_doc_details.po_number,
                'po_doc': str(purchasing_doc_details.po_doc),
                'invoice_number': purchasing_doc_details.invoice_number,
                'invoice_doc': str(purchasing_doc_details.invoice_doc),
                'packing_list': purchasing_doc_details.packing_list,
                'pl_doc': str(purchasing_doc_details.pl_doc),
                'k1_form': purchasing_doc_details.k1_form,
                'k1_doc': str(purchasing_doc_details.k1_doc),
                'AWB_number': purchasing_doc_details.AWB_number,
                'AWB_doc': str(purchasing_doc_details.AWB_doc),
                'create_date': purchasing_doc_details.create_date,
            })

        else:
            # If stock_in_tag is not provided, generate data for buttons
            for stock_in_item in stock_in_items:
                
                stock_tag_baseds = RawMaterialInventory.objects.filter(
                    stock_in_tag=stock_in_item.stock_in_tag,
                    stock_type=stock_in_item.stock_type,
                )
                
                for stock_tag_based in stock_tag_baseds:
                    response_data.append({
                        'identifier': stock_tag_based.component.identifier.parent_item_code,
                        'component': stock_tag_based.component.id,
                        #'quantity': stock_tag_based.quantity,
                        'lot': stock_tag_based.lot_number,
                        #'expiry_date': stock_tag_based.exp_date,
                        #'stock_in_date': stock_tag_based.stock_in_date,
                        #'stock_out_date': stock_tag_based.stock_out_date,
                        #'price_per_unit': stock_tag_based.price_per_unit,
                        'stock_in_tag': stock_tag_based.stock_in_tag.id,
                        #'stock_type': stock_tag_based.stock_type,
                        'supplier': stock_tag_based.purchasing_doc.supplier.company_name,
                        'purchasing_document': stock_tag_based.purchasing_doc.po_number,
                        'invoice_number': stock_tag_based.purchasing_doc.invoice_number,
                        'packing_list': stock_tag_based.purchasing_doc.packing_list,
                        'k1_form': stock_tag_based.purchasing_doc.k1_form,
                        'AWB_number': stock_tag_based.purchasing_doc.AWB_number,
                    })
        print(response_data)
        return JsonResponse(response_data, safe=False)

class RawMaterialInventoryIdentifierComponentBasedLogUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_update.html'
    context_object_name = 'raw_material_inventory'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['identifier_id'] = self.kwargs.get('identifier_id')
        kwargs['initial']['component_id'] = self.kwargs.get('component_id')
        kwargs['initial']['stock_type'] = self.kwargs.get('stock_type', '1')  # Default to stock-in

        return kwargs

    def get_success_url(self):
        return reverse_lazy('purchasing-raw-material-inventory-identifier-component-based-log-list', args=[self.object.component.identifier.id, self.object.component.id])

    def form_valid(self, form):
        RawMaterialInventory = self.get_object()
        messages.success(self.request, f'{RawMaterialInventory.component} updated successfully!')

        return super().form_valid(form)

class RawMaterialInventoryIdentifierComponentBasedLogDeleteView(LoginRequiredMixin,DeleteView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_delete.html'
    context_object_name = 'raw_material_inventory'

    def get_success_url(self):
        return reverse_lazy('purchasing-raw-material-inventory-identifier-component-based-log-list', args=[self.object.component.identifier.id, self.object.component.id])

    def delete(self, request, *args, **kwargs):
        RawMaterialInventory = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{RawMaterialInventory.component} deleted successfully!')

        return response

class RawMaterialInventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_update.html'
    success_url = reverse_lazy('purchasing-raw-material-inventory-list')
    context_object_name = 'RawMaterialInventory'

    def form_valid(self, form):
        RawMaterialInventory = self.get_object()
        messages.success(self.request, f'{RawMaterialInventory.component} updated successfully!')

        return super().form_valid(form)


class RawMaterialInventoryDeleteView(LoginRequiredMixin,DeleteView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_delete.html'
    context_object_name = 'RawMaterialInventory'
    success_url = reverse_lazy('purchasing-raw-material-inventory-list')

    def delete(self, request, *args, **kwargs):
        RawMaterialInventory = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{RawMaterialInventory.component} deleted successfully!')

        return response