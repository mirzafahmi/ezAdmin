from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

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

class RawMaterialComponentCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialComponent
    form_class = RawMaterialComponentForm
    template_name = 'purchasing/raw_material_component_create.html'
    success_url = reverse_lazy('purchasing-raw-material-component-list')

    def form_valid(self, form):
        component = form.cleaned_data['component']
        messages.success(self.request, f'{component} for {form.cleaned_data["identifier"]} created successfully!')

        return super().form_valid(form)

class RawMaterialComponentListView(LoginRequiredMixin, ListView):
    model = RawMaterialComponent
    template_name = 'purchasing/raw_material_component_list.html'
    context_object_name = 'components'  # The variable name in the template

    # You can customize the queryset if needed
    def get_queryset(self):

        return RawMaterialComponent.objects.all()

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

class RawMaterialInventoryCreateView(LoginRequiredMixin,CreateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_create.html'
    success_url = reverse_lazy('purchasing-raw-material-inventory-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['stock_type'] = self.kwargs.get('stock_type', '1')  # Default to stock-in
        return kwargs

    def form_valid(self, form):
        RawMaterialInventory = form.cleaned_data
        print(RawMaterialInventory)
        messages.success(self.request, f'{RawMaterialInventory["component"]} log of {RawMaterialInventory["purchasing_doc"]} created successfully!')

        return super().form_valid(form)

class RawMaterialInventoryAJAX(View):
    def get(self, request, *args, **kwargs):
        component_id = request.GET.get('component_id')
        stock_type = request.GET.get('type')

        print("Component ID:", component_id)
        print("Stock Type:", stock_type)

        if stock_type == '2':
            raw_material = RawMaterialInventory.objects.filter(
                component_id=component_id,
                stock_type='1',  # Stock In
            ).extra(
                select={'formatted_date': "(exp_date || '-01')"}
            ).order_by('formatted_date').first()

        if raw_material:
                fifo_info = {
                    'lot_number': raw_material.lot_number,
                    'exp_date': raw_material.exp_date,
                    'price_per_unit': raw_material.price_per_unit,
                    'purchasing_doc': raw_material.purchasing_doc_id,  # Assuming purchasing_doc is a ForeignKey
                }

                print(raw_material.purchasing_doc_id)
                return JsonResponse(fifo_info)

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
        queryset = RawMaterialInventory.objects.values_list('component__identifier__parent_item_code', 'component__identifier_id').distinct()

        return queryset

class RawMaterialInventoryIdentifierComponentBasedListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identifier_id = self.kwargs.get('identifier_id')
        identifier = get_object_or_404(RawMaterialIdentifier, id=identifier_id)

        queryset = RawMaterialInventory.objects.filter(component__identifier=identifier)
        
        # Extracting a list of distinct components and their IDs
        distinct_components = queryset.values_list('component__component', flat=True).distinct()
        distinct_components_ids = queryset.values_list('component_id', flat=True).distinct()

        # Creating a list of dictionaries for components with their ID and name
        components_list = [{'id': component_id, 'name': component_name} for component_id, component_name in zip(distinct_components_ids, distinct_components)]

        # Adding the extracted data to the context
        context['raw_material_inventory_list_identifier_component_baseds'] = components_list
        context['parent_item_code'] = identifier
        context['identifier_id'] = identifier_id

        return context

class RawMaterialInventoryIdentifierComponentBasedLogListView(LoginRequiredMixin, ListView):
    model = RawMaterialInventory
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_log_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        component_id = self.kwargs.get('component_id')

        #identifier = get_object_or_404(RawMaterialIdentifier, id=identifier_id)

        queryset = RawMaterialInventory.objects.filter(component__id=component_id)

        distinct_components = queryset.values_list('component__component').distinct()

        context['RawMaterialInventoriesIdentifierComponentBasedLogs'] = queryset
        context['component_id'] = component_id
        context['component'] = queryset.values_list('component__identifier__parent_item_code', 'component__component').distinct()

        return context

class RawMaterialInventoryIdentifierComponentBasedLogUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterialInventory
    form_class = RawMaterialInventoryForm
    template_name = 'purchasing/raw_material_inventory_identifier_component_based_update.html'
    context_object_name = 'raw_material_inventory'

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