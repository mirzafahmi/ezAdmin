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
from django.core.serializers import serialize
from mixins.validation_mixin import QuantityValidationMixin
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

from .models import *
from .forms import *
from store.models import Product
from production.models import RawMaterialInventory

import csv
import pandas as pd
import re
import json
import pprint
import math
from collections import Counter
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import sys
from datetime import datetime

class RawMaterialIdentifierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RawMaterialIdentifier
    form_class = RawMaterialIdentifierForm
    template_name = 'production/raw_material_identifier_create.html'
    
    permission_required = 'production.add_identifier'

    def get_success_url(self):
        if 'identifier_create' in self.request.get_full_path():
            return reverse('production-raw-material-inventory-identifier-based-list')
        else:
            return reverse('production-raw-material-identifier-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['cancel_url'] = self.get_success_url()  # Use the success URL as cancel URL for simplicity
        
        return context

    def form_valid(self, form):
        identifier = form.cleaned_data['parent_item_code'].upper()
        messages.success(self.request, f'{identifier} identifier created successfully!')

        return super().form_valid(form)

class RawMaterialIdentifierListView(LoginRequiredMixin, ListView):
    model = RawMaterialIdentifier
    template_name = 'production/raw_material_identifier_list.html'
    context_object_name = 'identifiers'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialIdentifier.objects.all()

class RawMaterialIdentifierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RawMaterialIdentifier
    form_class = RawMaterialIdentifierForm
    template_name = 'production/raw_material_identifier_update.html'
    success_url = reverse_lazy('production-raw-material-identifier-list')
    context_object_name = 'identifier'

    permission_required = 'production.change_identifier'

    def form_valid(self, form):
        identifier = self.get_object().parent_item_code
        messages.success(self.request, f'{identifier} identifier updated successfully!')

        return super().form_valid(form)


class RawMaterialIdentifierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RawMaterialIdentifier
    template_name = 'production/raw_material_identifier_delete.html'
    context_object_name = 'identifier'
    success_url = reverse_lazy('production-raw-material-identifier-list')

    permission_required = 'production.delete_identifier'

    def post(self, request, *args, **kwargs):
        identifier = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:  
            success_message = f'{identifier} identifier deleted successfully!'
            messages.success(self.request, success_message)

        return response

class RawMaterialComponentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RawMaterialComponent
    form_class = RawMaterialComponentForm
    template_name = 'production/raw_material_component_create.html'

    permission_required = 'production.add_component'

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
            return reverse('production-raw-material-inventory-identifier-component-based-list', kwargs={'identifier_id': identifier_id})
        else:
            return reverse_lazy('production-raw-material-component-list')
    
    def get_cancel_url(self):
        if 'identifier_id' in self.kwargs:
            identifier_id = self.kwargs['identifier_id']  # Get the 'identifier_name' parameter
            # Construct the success URL with the 'identifier_name'
            return reverse('production-raw-material-inventory-identifier-component-based-list', kwargs={'identifier_id': identifier_id})
        else:
            return reverse_lazy('production-raw-material-component-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.get_cancel_url()
        return context

    def form_valid(self, form):
        component = form.cleaned_data['component']
        messages.success(self.request, f'{component} component for {form.cleaned_data["identifier"]} created successfully!')

        return super().form_valid(form)

class RawMaterialComponentListView(LoginRequiredMixin, ListView):
    model = RawMaterialComponent
    template_name = 'production/raw_material_component_list.html'
    context_object_name = 'components'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialComponent.objects.all().order_by('identifier')

class RawMaterialComponentListViewAJAX(View):
    def get(self, request, *args, **kwargs):
        component_name = request.GET.get('component_name')

        filter_data =[] #empty array could cause bug of empty filter button

        if component_name:
            if component_name == "main-page":
                all_components = RawMaterialComponent.objects.all().order_by('identifier')

                for all_component in all_components:
                    filter_data.append({
                        'identifier': all_component.identifier.parent_item_code,
                        'identifier_id': all_component.identifier_id,
                        'component': all_component.component,
                        'component_id': all_component.id,
                        'specifications': all_component.spec,
                        'create_date': all_component.create_date,
                    })
            else:
                # Filter the model objects based on the component name
                filtered_objects = RawMaterialComponent.objects.filter(component__icontains=component_name)

                filter_components = filtered_objects

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
            components = RawMaterialComponent.objects.all()

            component = RawMaterialComponent.objects.values_list('component', flat=True)

            # Extract words and phrases (splitting on commas)
            all_words = ','.join(component)
            all_words_list = all_words.split(',')
            
            simple_words = set() #store only distint data

            for word in all_words_list:
                if 'for' not in word.lower():  # Exclude words with 'for'
                    simple_words.add(word)
                else:
                    simple_words.add(word.split('For')[0].strip())

            component_labels = list(simple_words)
            
            return JsonResponse(component_labels, safe=False)


class RawMaterialComponentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RawMaterialComponent
    form_class = RawMaterialComponentForm
    template_name = 'production/raw_material_component_update.html'
    success_url = reverse_lazy('production-raw-material-component-list')
    context_object_name = 'component'

    permission_required = 'production.change_component'

    def form_valid(self, form):
        component = self.get_object()
        messages.success(self.request, f'{component.component} component for {component.identifier} updated successfully!')

        return super().form_valid(form)

class RawMaterialComponentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RawMaterialComponent
    template_name = 'production/raw_material_component_delete.html'
    context_object_name = 'component'
    success_url = reverse_lazy('production-raw-material-component-list')

    permission_required = 'production.delete_component'
    
    def post(self, request, *args, **kwargs):
        component = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{component.component} component for {component.identifier} deleted successfully!'
            messages.success(self.request, success_message)

        return response

class BOMComponentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BOMComponent
    form_class = BOMComponentForm
    template_name = 'production/BOM_component_create.html'
    success_url = reverse_lazy('production-BOM-component-list')

    permission_required = 'production.add_BOMcomponent'

    def form_valid(self, form):
        BOMcomponent = form.save()
        messages.success(self.request, f"{BOMcomponent.raw_material_component}'s BOMComponent for {BOMcomponent.product.item_code} created successfully!")

        return super().form_valid(form)

class BOMComponentListView(LoginRequiredMixin, ListView):
    model = BOMComponent
    template_name = 'production/BOM_component_list.html'
    context_object_name = 'BOMComponents'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return BOMComponent.objects.all().order_by('product', 'raw_material_component')

class BOMComponentListViewAJAX(View):
    def get(self, request, *args, **kwargs):
        item_code = request.GET.get('item_code')
        
        if item_code:
            if item_code == 'main-page':
                BOM_components = BOMComponent.objects.all().order_by('product', 'raw_material_component')

                filtered_data = []

                for BOM_component in BOM_components:
                    print(BOM_component)
                    filtered_data.append({
                        'BOMComponent_id': BOM_component.id,
                        'product': BOM_component.product.item_code,
                        'raw_material_component': BOM_component.raw_material_component.component,
                        'quantity_used': BOM_component.quantity_used,
                        'create_date': BOM_component.create_date
                    })

                return JsonResponse(filtered_data, safe=False)
            else:
                items_code_filtered = BOMComponent.objects.filter(
                    product__item_code=item_code
                    ).order_by(
                    'create_date')     
                
                filtered_data = []

                for item_code_filtered in items_code_filtered:
                    filtered_data.append({
                        'BOMComponent_id': item_code_filtered.id,
                        'product': item_code_filtered.product.item_code,
                        'raw_material_component': item_code_filtered.raw_material_component.component,
                        'quantity_used': item_code_filtered.quantity_used,
                        'create_date': item_code_filtered.create_date
                    })

                return JsonResponse(filtered_data, safe=False)
        else:
            product = Product.objects.values_list('item_code', flat=True)

            return JsonResponse(list(product), safe=False)

class BOMComponentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BOMComponent
    form_class = BOMComponentForm
    template_name = 'production/BOM_component_update.html'
    success_url = reverse_lazy('production-BOM-component-list')
    context_object_name = 'BOMcomponent'

    permission_required = 'production.change_BOMcomponent'

    def form_valid(self, form):
        BOMcomponent = self.get_object()
        messages.success(self.request, f"{BOMcomponent.raw_material_component}'s BOMComponent for {BOMcomponent.product.item_code} updated successfully!")

        return super().form_valid(form)

class BOMComponentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BOMComponent
    template_name = 'production/BOM_component_delete.html'
    context_object_name = 'BOMcomponent'
    success_url = reverse_lazy('production-BOM-component-list')

    permission_required = 'production.delete_BOMcomponent'
    
    def post(self, request, *args, **kwargs):
        BOMcomponent = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f"{BOMcomponent.raw_material_component}'s BOMComponent for {BOMcomponent.product.item_code} deleted successfully!"
            messages.success(self.request, success_message)

        return response

class ProductionLogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductionLog
    form_class = ProductionLogForm
    template_name = 'production/production_log_create.html'
    success_url = reverse_lazy('production-production-log-list')

    permission_required = 'production.add_productionlog'
    
    def post(self, request, *args, **kwargs):
        try:
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            inventory_details = data.get('inventory_details', {})
            form_data = data.get('formData', '')
            print(inventory_details)

            form_data_dict = {}

            for param in form_data.split('&'):
                key, value = param.split('=')

                # If the key already exists, append the value to a list
                if key in form_data_dict:
                    if not isinstance(form_data_dict[key], list):
                        form_data_dict[key] = [form_data_dict[key]]
                    form_data_dict[key].append(value)
                else:
                    form_data_dict[key] = value

            bom_component_ids = form_data_dict.get('BOMComponents', [])

            # Ensure bom_component_ids is a list
            if not isinstance(bom_component_ids, list):
                bom_component_ids = [bom_component_ids]

            form_data_dict['BOMComponents'] = bom_component_ids

            form = self.form_class(data=form_data_dict)

            quantity_produced = int(form_data_dict.get('quantity_produced', 0))
            product_id = form_data_dict.get('product')
            product_packing = Product.objects.get(id=product_id).packing

            if form.is_valid():
                instance = form.save(commit=False)

                # Save the instance to get an ID
                instance.save()

                # Associate selected BOMComponents with the ProductionLog
                instance.BOMComponents.set(bom_component_ids)

                # Save the instance again to update the M2M relationship
                instance.save()
                
                for component, details in inventory_details.items():
                    stock_in_inventory = RawMaterialInventory.objects.filter(
                        stock_in_tag=details['stock_in_tag'],
                        stock_type="1").first()

                    component_id = stock_in_inventory.component.id
                    stock_in_details = stock_in_inventory
                    quantity_per_unit = BOMComponent.objects.get(raw_material_component__id=component_id).quantity_used
                    inventory_entry = RawMaterialInventory.objects.create(
                        component_id=component_id,
                        quantity= details['quantity'],
                        lot_number=stock_in_inventory.lot_number,
                        exp_date=stock_in_inventory.exp_date,
                        price_per_unit=stock_in_inventory.price_per_unit,
                        stock_type='2',
                        purchasing_doc=stock_in_inventory.purchasing_doc,
                        stock_in_tag=stock_in_inventory.stock_in_tag,
                        production_log=instance,
                    )
                

                print('Form saved successfully')
                success_message = f'Batch {instance.lot_number} production log created successfully for {instance.BOMComponents.all()[0].product.item_code}!'
                
                return JsonResponse({'success': True, 'message': success_message})

            else:
                print('Validation failed')
                print(form.errors)
                return JsonResponse({'success': False, 'message': 'Validation failed', 'errors': form.errors})

        except Exception as e:
            print(f'An error occurred: {e}')
            return JsonResponse({'success': False, 'message': 'An error occurred'})

class ProductionLogCreateViewAJAX(View, QuantityValidationMixin):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        #component_id = request.GET.get('component_id')
        BOMComponent_id = request.GET.get('BOMComponent_id')
        stock_in_tag = request.GET.get('stock_in_tag')

        if BOMComponent_id:

            component_id = BOMComponent.objects.filter(
                id=BOMComponent_id
                ).values_list(
                'raw_material_component__id',
                 flat=True)[0]
            
            quantity_used = BOMComponent.objects.filter(
                id=BOMComponent_id
                ).values_list(
                'quantity_used',
                 flat=True)[0]

            raw_material_inventories = RawMaterialInventory.objects.filter(
                component__id=component_id, 
                stock_type='1'
                ).order_by('exp_date')

            data=[]

            for raw_material_inventory in raw_material_inventories:
                stock_out_log = RawMaterialInventory.objects.filter(
                    stock_in_tag=raw_material_inventory.stock_in_tag,
                    stock_type='2')

                stock_in = raw_material_inventory.quantity
                stock_out = stock_out_log.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

                balance = stock_in - stock_out

                if balance <= 0:
                    pass
                else:
                    data.append({
                        'stock_in_tag': raw_material_inventory.stock_in_tag_id,
                        'lot_number': raw_material_inventory.lot_number,
                        'exp_date': raw_material_inventory.exp_date,
                        'available_quantity': balance,
                        'component_name': raw_material_inventory.component.component,
                        'po_number': raw_material_inventory.purchasing_doc.po_number,
                        'invoice_number': raw_material_inventory.purchasing_doc.invoice_number,
                        'quantity_used': quantity_used,
                        })
            
            return JsonResponse(data, safe=False)
        
        elif stock_in_tag:

            stock_in_log = RawMaterialInventory.objects.filter(
                    stock_in_tag=stock_in_tag,
                    stock_type='1').aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            stock_out_log = RawMaterialInventory.objects.filter(
                    stock_in_tag=stock_in_tag,
                    stock_type='2').aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            
            balance = stock_in_log - stock_out_log

            data = {
                'available_quantity': balance
            }

            return JsonResponse(data, safe=False)


        else: #for the bomcomponent list
            bom_components = BOMComponent.objects.filter(
                product__id=product_id
                ).values_list(
                    'product__item_code', 
                    'raw_material_component__id', 
                    'raw_material_component__component', 
                    'raw_material_component__identifier__parent_item_code', 
                    'quantity_used',
                    'id',
                )
            
            bom_components_list = [{
                'item_code': component[0], 
                'component_id': component[1], 
                'component_name': component[2],
                'component_identifier': component[3], 
                'quantity_used': component[4],
                'BOMComponent_id': component[5]
                } for component in bom_components]

            data = {
                'bom_components': list(bom_components_list)
                }

            return JsonResponse(data, safe=False)

class ProductionLogListView(LoginRequiredMixin, ListView):
    model = ProductionLog
    template_name = 'production/production_log_list.html'
    context_object_name = 'ProductionLogs'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve related RawMaterialInventory instances for each ProductionLog
        production_logs = context['ProductionLogs']
        related_inventory_entries = RawMaterialInventory.objects.filter(production_log__in=production_logs)

        # Add the related_inventory_entries to the context
        context['RelatedInventoryEntries'] = related_inventory_entries

        context['exists_flag'] = ProductionLog.objects.all().exists()

        return context

class ProductionLogListViewAJAX(View):
    def get(self, request, *args, **kwargs):
        item_code = request.GET.get('item_code')
        if item_code:
            if item_code == "main-page":
                logs_filter = ProductionLog.objects.all().order_by('create_date')

                filtered_data = []
                
                for log_filter in logs_filter:
                    raw_material_details = []
                    components = RawMaterialInventory.objects.filter(production_log=log_filter.id)

                    for component in components:
                        raw_material_details.append({
                            'identifier': component.component.identifier.parent_item_code,
                            'component': component.component.component,
                            'lot_number': component.lot_number,
                            'exp_date': component.exp_date,
                        })

                    print(raw_material_details)
                    #print(bom_component)
                    filtered_data.append({
                        'log_id': log_filter.id,
                        'item_code': log_filter.BOMComponents.all()[0].product.item_code,
                        'lot_number': log_filter.lot_number,
                        'exp_date': log_filter.exp_date,
                        'quantity_produced': log_filter.quantity_produced,
                        'component_details': raw_material_details,
                        'rH': json.dumps(log_filter.rH, cls=DjangoJSONEncoder),
                        'temperature': json.dumps(log_filter.temperature, cls=DjangoJSONEncoder),
                        'create_date': log_filter.create_date
                        })

                return JsonResponse(filtered_data, safe=False)

            else:
                logs_filter = ProductionLog.objects.filter(
                    BOMComponents__product__item_code=item_code
                    )
                
                log_filter = logs_filter.first()

                print(log_filter.BOMComponents.all()[0].product.item_code)
                filtered_data = []
                
                raw_material_details = []
                components = RawMaterialInventory.objects.filter(production_log__in=logs_filter)

                for component in components:
                    raw_material_details.append({
                        'identifier': component.component.identifier.parent_item_code,
                        'component': component.component.component,
                        'lot_number': component.lot_number,
                        'exp_date': component.exp_date,
                    })

                print(raw_material_details)
                #print(bom_component)
                filtered_data.append({
                    'log_id': log_filter.id,
                    'item_code': log_filter.BOMComponents.all()[0].product.item_code,
                    'lot_number': log_filter.lot_number,
                    'exp_date': log_filter.exp_date,
                    'quantity_produced': log_filter.quantity_produced,
                    'component_details': raw_material_details,
                    'rH': json.dumps(log_filter.rH, cls=DjangoJSONEncoder),
                    'temperature': json.dumps(log_filter.temperature, cls=DjangoJSONEncoder),
                    'create_date': log_filter.create_date
                    })

                return JsonResponse(filtered_data, safe=False)
        
        else:
            product = ProductionLog.objects.values_list('BOMComponents__product__item_code', flat=True).distinct()

            return JsonResponse(list(product), safe=False)

class ProductionLogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductionLog
    form_class = ProductionLogForm
    template_name = 'production/production_log_update.html'
    success_url = reverse_lazy('production-production-log-list')
    context_object_name = 'ProductionLog'

    permission_required = 'production.change_productionlog'

    def form_valid(self, form):
        production_log = self.get_object()
        messages.success(self.request, f'Batch {production_log.lot_number} production log for {production_log.BOMComponents.all()[0].product.item_code} updated successfully!')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve related RawMaterialInventory instances for each ProductionLog
        production_logs = context['ProductionLog']

        production_log_id = self.kwargs.get('pk')
        related_inventory_entries = RawMaterialInventory.objects.filter(production_log=production_log_id)
        pprint.pprint(serialize('json', related_inventory_entries))
        context['RelatedInventoryEntries'] = serialize('json', related_inventory_entries)

        raw_material_component = RawMaterialComponent.objects.all()
        pprint.pprint(serialize('json', raw_material_component))
        context['RawMaterialComponent'] = serialize('json', raw_material_component)
        
        return context

class ProductionLogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductionLog
    template_name = 'production/production_log_delete.html'
    context_object_name = 'ProductionLog'
    success_url = reverse_lazy('production-production-log-list')

    permission_required = 'production.delete_productionlog'

    def form_valid(self, form):
        production_log = self.get_object()
        
        raw_material_inventory_entries = RawMaterialInventory.objects.filter(production_log=production_log)
        
        for entry in raw_material_inventory_entries:
            entry.delete()

        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        production_log = self.get_object()

        item_code = production_log.BOMComponents.all()[0].product.item_code

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302: 
            success_message = f'Batch {production_log.lot_number} production log for {item_code} deleted successfully!'
            messages.success(self.request, success_message)

        return response

class RawMaterialInventoryLogMainView(LoginRequiredMixin, TemplateView):
    template_name = 'production/raw_material_inventory_log_main.html'

class InventoryMainView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/inventory_main.html'

class RawMaterialMainView(LoginRequiredMixin, TemplateView):
    template_name = 'production/production_main.html'

class RawMaterialInventoryCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'production/raw_material_inventory_create.html'
    success_url = reverse_lazy('production-raw-material-inventory-list')

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
    template_name = 'production/raw_material_inventory_list.html'
    context_object_name = 'RawMaterialInventories'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialInventory.objects.all()

class RawMaterialInventoryIdentifierBasedListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'production/raw_material_inventory_identifier_based_main.html'
    context_object_name = 'RawMaterialInventoriesIdentifierBaseds'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):
        # Use select_related to fetch the related RawMaterialComponent and RawMaterialIdentifier
        queryset = RawMaterialIdentifier.objects.values_list('parent_item_code', 'id').distinct()

        return queryset

class RawMaterialInventoryIdentifierComponentBasedListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'production/raw_material_inventory_identifier_component_based_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        identifier = get_object_or_404(RawMaterialIdentifier, id=identifier_id)

        queryset = RawMaterialComponent.objects.filter(identifier=identifier)
        
        # Extracting a list of distinct components and their IDs
        distinct_components = queryset.values_list('component', flat=True).distinct()
        distinct_components_ids = queryset.values_list('id', flat=True).distinct()
        
        # Creating a list of dictionaries for components with their ID and name
        components_list = [{'id': component_id, 'name': component_name} for component_id, component_name in zip(distinct_components_ids, distinct_components)]

        # Adding the extracted data to the context
        context['raw_material_inventory_list_identifier_component_baseds'] = components_list
        context['parent_item_code'] = identifier
        context['identifier_id'] = identifier_id
        context['exists_flag'] = queryset.exists()

        return context

class RawMaterialInventoryIdentifierComponentBasedLogCreateMainView(LoginRequiredMixin, TemplateView, QuantityValidationMixin):
    template_name = 'production/raw_material_inventory_identifier_component_based_log_create_main.html'
    
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
    
class RawMaterialInventoryIdentifierComponentBasedLogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView, QuantityValidationMixin):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'production/raw_material_inventory_identifier_component_based_log_create.html'

    permission_required = 'production.add_rawmaterialinventory'

    def get_success_url(self):
        identifier_id = self.kwargs.get('identifier_id')
        component_id = self.kwargs.get('component_id')
        stock_type = self.kwargs.get('stock_type', '1')

        return reverse_lazy('production-raw-material-inventory-identifier-component-based-log-list', args=[identifier_id, component_id])

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
        lot_number = request.GET.get('lot_number')
        quantity = int(request.GET.get('quantity', 0))
        inventory_log = request.GET.get('inventory_log', None)

        response_data = {
            'component': component_id,
            'available_quantity': None,
            'alert': False,
            'related_stock_in': None,
        }

        if stock_type == '2':
            current_raw_material, current_raw_material_quantity = self.get_available_quantity_fifo(component_id)

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

            if lot_number:
                if inventory_log:
                    lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number, inventory_log)
                    previous_quantity = RawMaterialInventory.objects.get(id=inventory_log).quantity
                else: 
                    lot_number_data, lot_number_balance_stock = self.get_overide_data(component_id, lot_number)
                    previous_quantity = 0

                response_data = {
                    'component': lot_number_data.component.id,
                    'lot_number': lot_number_data.lot_number,
                    'exp_date': lot_number_data.exp_date,
                    'price_per_unit': lot_number_data.price_per_unit,
                    'purchasing_doc': lot_number_data.purchasing_doc_id,
                    'previous_quantity': previous_quantity,
                    'available_quantity': lot_number_balance_stock,
                    'stock_in_tag': lot_number_data.stock_in_tag.id,
                }

        if stock_type == None:
            current_raw_material, current_raw_material_quantity = self.get_available_quantity_fifo(component_id)
            component = RawMaterialComponent.objects.get(id=component_id)

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
    template_name = 'production/raw_material_inventory_identifier_component_based_log_list.html'

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

        response_data = []

        if stock_in_tag:
            if stock_in_tag == "main-page":
                all_logs = RawMaterialInventory.objects.filter(
                    component__identifier__parent_item_code = identifier_id,
                    component_id = component_id
                )

                stock_in_all = all_logs.filter(
                    stock_type='1',
                ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

                stock_out_all = all_logs.filter(
                    stock_type='2',
                ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

                balance_quantity_all = stock_in_all - stock_out_all

                for all_log in all_logs:
                    response_data.append({
                        'log_id': all_log.id,
                        'identifier': all_log.component.identifier.parent_item_code,
                        'identifier_id': all_log.component.identifier.id,
                        'component': all_log.component.component,
                        'component_id': all_log.component.id,
                        'quantity': all_log.quantity,
                        'lot': all_log.lot_number,
                        'expiry_date': all_log.exp_date,
                        'stock_in_date': all_log.stock_in_date,
                        'stock_out_date': all_log.stock_out_date,
                        'currency_trade': all_log.purchasing_doc.supplier.currency_trade.currency_code,
                        'price_per_unit': all_log.price_per_unit,
                        'local_price_per_unit': all_log.price_per_unit * all_log.purchasing_doc.k1_form_rate,
                        'purchasing_document': all_log.purchasing_doc.po_number,
                        'purchasing_document_id': all_log.purchasing_doc.id,
                        'company_name': all_log.purchasing_doc.supplier.company_name,
                        'stock_in_tag': all_log.stock_in_tag.id,
                        'stock_type': all_log.stock_type,
                        'balance': balance_quantity_all,
                    })

            else:
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
                        'currency_trade': stock_tag_based.purchasing_doc.supplier.currency_trade.currency_code,
                        'price_per_unit': stock_tag_based.price_per_unit,
                        'local_price_per_unit': stock_tag_based.price_per_unit * stock_tag_based.purchasing_doc.k1_form_rate,
                        'purchasing_document': stock_tag_based.purchasing_doc.po_number,
                        'purchasing_document_id': stock_tag_based.purchasing_doc.id,
                        'company_name': stock_tag_based.purchasing_doc.supplier.company_name,
                        'stock_in_tag': stock_tag_based.stock_in_tag.id,
                        'stock_type': stock_tag_based.stock_type,
                        'balance': balance_quantity_tag_based,
                    })
                    
        elif purchasing_doc:
            purchasing_doc_details = PurchasingDocument.objects.filter(id=purchasing_doc).first()

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
                'k1_form_rate': purchasing_doc_details.k1_form_rate,
                'AWB_number': purchasing_doc_details.AWB_number,
                'AWB_doc': str(purchasing_doc_details.AWB_doc),
                'create_date': purchasing_doc_details.create_date,
            })
            
        else:
            # If stock_in_tag is not provided, generate data for buttons
            stock_in_items = RawMaterialInventory.objects.filter(
                    component_id=component_id,
                    stock_type='1',
                ).order_by('exp_date')
                
            for stock_in_item in stock_in_items:
                
                stock_tag_baseds = RawMaterialInventory.objects.filter(
                    stock_in_tag=stock_in_item.stock_in_tag,
                    stock_type=stock_in_item.stock_type,
                )
                
                for stock_tag_based in stock_tag_baseds:
                    response_data.append({
                        'identifier': stock_tag_based.component.identifier.parent_item_code,
                        'component': stock_tag_based.component.id,
                        'lot': stock_tag_based.lot_number,
                        'stock_in_tag': stock_tag_based.stock_in_tag.id,
                        'supplier': stock_tag_based.purchasing_doc.supplier.company_name,
                        'purchasing_document': stock_tag_based.purchasing_doc.po_number,
                        'invoice_number': stock_tag_based.purchasing_doc.invoice_number,
                        'packing_list': stock_tag_based.purchasing_doc.packing_list,
                        'k1_form': stock_tag_based.purchasing_doc.k1_form,
                        'AWB_number': stock_tag_based.purchasing_doc.AWB_number,
                    })

        return JsonResponse(response_data, safe=False)

class RawMaterialInventoryIdentifierComponentBasedLogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'production/raw_material_inventory_identifier_component_based_update.html'
    context_object_name = 'raw_material_inventory'

    permission_required = 'production.change_rawmaterialinventory'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['identifier_id'] = self.kwargs.get('identifier_id')
        kwargs['initial']['component_id'] = self.kwargs.get('component_id')
        kwargs['initial']['stock_type'] = self.kwargs.get('stock_type', '1')  # Default to stock-in

        return kwargs

    def get_success_url(self):
        return reverse_lazy('production-raw-material-inventory-identifier-component-based-log-list', args=[self.object.component.identifier.id, self.object.component.id])

    def form_valid(self, form):
        RawMaterialInventory = self.get_object()
        messages.success(self.request, f'{RawMaterialInventory.component} for batch {RawMaterialInventory.lot_number}({RawMaterialInventory.production_log}) log updated successfully!')

        return super().form_valid(form)

class RawMaterialInventoryIdentifierComponentBasedLogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RawMaterialInventory
    template_name = 'production/raw_material_inventory_identifier_component_based_delete.html'
    context_object_name = 'raw_material_inventory'

    permission_required = 'production.delete_rawmaterialinventory'

    def get_success_url(self):
        return reverse_lazy('production-raw-material-inventory-identifier-component-based-log-list', args=[self.object.component.identifier.id, self.object.component.id])

    def post(self, request, *args, **kwargs):
        RawMaterialInventory = self.get_object()

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302: 
            success_message = f'{RawMaterialInventory.component} for batch {RawMaterialInventory.lot_number}({RawMaterialInventory.production_log}) log deleted successfully!'
            messages.success(self.request, success_message)

        return response


class RawMaterialInventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'production/raw_material_inventory_update.html'
    success_url = reverse_lazy('production-raw-material-inventory-list')
    context_object_name = 'RawMaterialInventory'

    def form_valid(self, form):
        RawMaterialInventory = self.get_object()
        messages.success(self.request, f'{RawMaterialInventory.component} updated successfully!')

        return super().form_valid(form)


class RawMaterialInventoryDeleteView(LoginRequiredMixin,DeleteView):
    model = RawMaterialInventory
    template_name = 'production/raw_material_inventory_delete.html'
    context_object_name = 'RawMaterialInventory'
    success_url = reverse_lazy('production-raw-material-inventory-list')

    def delete(self, request, *args, **kwargs):
        RawMaterialInventory = self.get_object()
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 302:
            messages.success(self.request, f'{RawMaterialInventory.component} deleted successfully!')

        return response
        
@login_required
def generate_balance_assets_excel(request):
    selected_date_str = request.GET.get('selected_date')
    username = request.user.username

    # Parse the input string into a datetime object (naive)
    selected_date_naive = datetime.strptime(selected_date_str, '%Y-%m-%d')

    # Make the datetime object aware by associating it with a time zone
    selected_date_aware = timezone.make_aware(selected_date_naive, timezone.get_current_timezone()).replace(hour=23, minute=59, second=59)

    print(selected_date_aware)

    # Dictionary to store data based on parent_item_code and component
    data_dict = {}

    current_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')

    instances = RawMaterialInventory.objects.all().order_by('component__identifier__parent_item_code', 'component__component').filter(stock_type='1')
    print(instances)
    
    for instance in instances:    
        stock_in = RawMaterialInventory.objects.filter(
            stock_in_tag=instance.stock_in_tag_id,
            stock_type='1',
            stock_in_date__lte=selected_date_aware).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        stock_out = RawMaterialInventory.objects.filter(
            stock_in_tag=instance.stock_in_tag_id,
            stock_type='2',
            stock_out_date__lte=selected_date_aware).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        balance = stock_in - stock_out

        print(balance)
        if balance != 0:
            parent_item_code = instance.component.identifier.parent_item_code

            if parent_item_code not in data_dict:
                data_dict[parent_item_code] = {}

            component = instance.component.component

            if component not in data_dict[parent_item_code]:
                data_dict[parent_item_code][component] = []

            price_per_unit_myr = float(instance.price_per_unit) * float(instance.purchasing_doc.k1_form_rate)
            total_as_date = int(balance) * float(price_per_unit_myr)

            flattened_row = {
                'LOT_NUMBER': instance.lot_number,
                'BALANCE (QUANTITY)': balance,
                'PRICE_PER_UNIT (USD)': f'{float(instance.price_per_unit):.2f}' if float(instance.price_per_unit) > 0.01 else float(instance.price_per_unit),
                'PRICE_PER_UNIT (MYR)': f'{float(price_per_unit_myr):.2f}' if float(price_per_unit_myr) > 0.01 else float(price_per_unit_myr),
                'TOTAL AS DATE (MYR)': f'{total_as_date:.2f}' if total_as_date > 0.01 else total_as_date,
                'INVOICE_NUMBER': instance.purchasing_doc.invoice_number,
                'SUPPLIER': instance.purchasing_doc.supplier.company_name,
                'K1 FORM RATE': f'{float(instance.purchasing_doc.k1_form_rate):.2f}' if float(instance.purchasing_doc.k1_form_rate) > 0.01 else float(instance.purchasing_doc.k1_form_rate),
                'PO_NUMBER': instance.purchasing_doc.po_number,
                'PACKING_LIST': instance.purchasing_doc.packing_list,
                'K1_FORM': instance.purchasing_doc.k1_form,
                'AWB_NUMBER': instance.purchasing_doc.AWB_number
            }

            data_dict[parent_item_code][component].append(flattened_row)

    # Combine all the data into a single list of dictionaries
    all_data = []
    for identifier, components_data in data_dict.items():
        for component, component_data in components_data.items():
            for row in component_data:
                row['IDENTIFIER'] = identifier
                row['COMPONENT'] = component
                all_data.append(row)

    # Specify the order of columns
    columns_order = [
        'IDENTIFIER', 
        'COMPONENT', 
        'LOT_NUMBER', 
        'BALANCE (QUANTITY)', 
        'PRICE_PER_UNIT (USD)', 
        'PRICE_PER_UNIT (MYR)', 
        'TOTAL AS DATE (MYR)', 
        'INVOICE_NUMBER',
        'SUPPLIER',
        'K1 FORM RATE',
        'PO_NUMBER', 
        'PACKING_LIST', 
        'K1_FORM', 
        'AWB_NUMBER'
        ]

    # Create a DataFrame with a specified order of columns
    df = pd.DataFrame(all_data, columns=columns_order)

    # Save the DataFrame to an Excel file
    output_excel_file_path = f'excel/raw-material-assets-(up-until:-{selected_date_aware}).xlsx'

    # Create a new Excel workbook and add a worksheet
    wb = Workbook()
    ws = wb.active

    # Write the DataFrame to the worksheet
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)

    # Add a gap of around 5 rows
    gap_rows = 5
    for _ in range(gap_rows):
        ws.append([])  # Append an empty row

    # Append footer_info
    footer_info = [
        {'Date of Generation:': current_time},
        {'Generated By:': username},
        {'Query Date Upper Limit:': selected_date_aware.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')},
    ]
    for info in footer_info:
        ws.append([])  # Add an empty row before each item in footer_info
        for key, value in info.items():
            ws.append([key, value])

    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell)) > max_length:
                    max_length = len(cell)
            except:
                pass
        adjusted_width = (max_length + 25)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    # Create an in-memory stream to save the workbook content
    from io import BytesIO
    output_stream = BytesIO()
    wb.save(output_stream)
    output_stream.seek(0)

    # Create a Django HttpResponse to return the file to the user
    response = HttpResponse(output_stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'inline; filename=raw-material-assets-(up-until:-{selected_date_aware}).xlsx'

    return response