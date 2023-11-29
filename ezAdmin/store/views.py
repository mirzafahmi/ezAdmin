from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from .models import *
from django.urls import reverse_lazy, reverse
from django.views import View
from production.models import RawMaterialIdentifier
from django.http import JsonResponse, HttpResponse

class StoreMainView(LoginRequiredMixin, TemplateView):
    template_name = 'store/store_main.html'

class BrandNameListView(LoginRequiredMixin, ListView):
    model = BrandName
    template_name = 'store/brand_name_list.html'
    context_object_name = 'brands'  # The variable name in the template

class BrandNameCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BrandName
    form_class = BrandNameForm
    template_name = 'store/brand_name_create.html'
    success_url = reverse_lazy('store-brand-name-list')

    permission_required = 'store.add_brandname'

    def form_valid(self, form):
        brand_name = form.cleaned_data['brand_name']
        company_name = form.cleaned_data['company_name']
        messages.success(self.request, f'{brand_name} brand from {company_name} created successfully!')

        return super().form_valid(form)

class BrandNameUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BrandName
    form_class = BrandNameForm
    template_name = 'store/brand_name_update.html'
    success_url = reverse_lazy('store-brand-name-list')
    context_object_name = 'brand'

    permission_required = 'purchasing.change_brandname'

    def form_valid(self, form):
        brand_name = self.get_object().brand_name
        company_name = self.get_object().company_name

        messages.success(self.request, f'{brand_name} brand from {company_name} updated successfully!')

        return super().form_valid(form)

class BrandNameDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BrandName
    template_name = 'store/brand_name_delete.html'
    success_url = reverse_lazy('store-brand-name-list')
    context_object_name = 'brand'

    permission_required = 'purchasing.delete_brandname'
    
    def post(self, request, *args, **kwargs):
        brand_name = self.get_object().brand_name
        company_name = self.get_object().company_name

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{brand_name} brand from {company_name} deleted successfully!'
            messages.success(self.request, success_message)

        return response

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    #context_object_name = 'products'  # The variable name in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        items = Product.objects.all()
        stocks_total = {}
        
        for item in items:
            stock_in = FinishedGoodsInventory.objects.filter(product_id = item.id).filter(stock_type = '1').aggregate(sum = Sum('quantity'))['sum'] or 0
            stock_out = FinishedGoodsInventory.objects.filter(product_id = item.id).filter(stock_type = '2').aggregate(sum = Sum('quantity'))['sum'] or 0

            stocks_total.update({item.id: stock_in - stock_out})

        context["products"] = items
        context["stocks"] = stocks_total

        return context
    
class ProductListViewAJAX(View):
    def get(self, request, *args, **kwargs):
        identifier_name = request.GET.get('identifier')

        filter_data =[] 
        
        if identifier_name:
            if identifier_name == "main-page":
                all_products = Product.objects.all().order_by('identifier')

                for all_product in all_products:
                    filter_data.append({
                        'identifier': all_product.identifier.parent_item_code,
                        'item_code': all_product.item_code,
                        'product_name': all_product.name,
                        'product_id': all_product.id,
                        'brand': all_product.brand.brand_name,
                        'packing': all_product.packing,
                        'uom': all_product.uom.name,
                        'create_date': all_product.create_date,
                    })
            else:
                # Filter the model objects based on the product name
                filtered_objects = Product.objects.filter(identifier__parent_item_code=identifier_name)

                filter_products = filtered_objects

                for filter_product in filter_products:
                    filter_data.append({
                        'identifier': filter_product.identifier.parent_item_code,
                        'item_code': filter_product.item_code,
                        'product_name': filter_product.name,
                        'product_id': filter_product.id,
                        'brand': filter_product.brand.brand_name,
                        'packing': filter_product.packing,
                        'uom': filter_product.uom.name,
                        'create_date': filter_product.create_date,
                    })

            
            return JsonResponse(filter_data, safe=False)
        else:
            identifiers = RawMaterialIdentifier.objects.values_list('parent_item_code', flat=True)

            return JsonResponse(list(identifiers), safe=False)

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_create.html'
    success_url = reverse_lazy('store-product-list')

    permission_required = 'store.add_product'

    def form_valid(self, form):
        product_name = form.cleaned_data['name']
        item_code = form.cleaned_data['item_code']
        messages.success(self.request, f'{product_name} ({item_code}) created successfully!')

        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_update.html'
    success_url = reverse_lazy('store-product-list')
    context_object_name = 'product'

    permission_required = 'purchasing.change_brandname'

    def form_valid(self, form):
        product_name = form.cleaned_data['name']
        item_code = form.cleaned_data['item_code']

        messages.success(self.request, f'{product_name} ({item_code}) updated successfully!')

        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_delete.html'
    success_url = reverse_lazy('store-product-list')
    context_object_name = 'product'

    permission_required = 'purchasing.delete_product'
    
    def post(self, request, *args, **kwargs):
        product_name = self.get_object().product_name
        item_code = self.get_object().item_code

        response = super().post(request, *args, **kwargs)

        if response.status_code == 302:
            success_message = f'{product_name} ({item_code}) deleted successfully!'
            messages.success(self.request, success_message)

        return response

@login_required
def product_list(request):
    items = Product.objects.all()
    stocks_total = {}
    for item in items:
        stock_in = FinishedGoodsInventory.objects.filter(product_id = item.id).filter(stock_type = '1').aggregate(sum = Sum('quantity'))['sum'] or 0
        stock_out = FinishedGoodsInventory.objects.filter(product_id = item.id).filter(stock_type = '2').aggregate(sum = Sum('quantity'))['sum'] or 0

        stocks_total.update({item.id: stock_in - stock_out})

    
    context = {
        'items': items,
        'stocks': stocks_total
    }

    return render(request, 'store/product.html', context)

@login_required
def product_add(request):
    items = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            item_code = form.cleaned_data.get('item_code')
            messages.success(request, f'{product_name} ({item_code}) has been added')
            return redirect ('store-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form
    }

    return render(request, 'store/product-form.html', context)

@login_required
def product_update(request, pk):
    items = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance = items)
        if form.is_valid():
            form.save()
            messages.success(request, f'{items.name} ({items.item_code}) has been updated')
            return redirect('store-product')
    else:
        form = ProductForm(instance = items)    
    context = {
        'form': form
    }
    return render(request, 'store/product-update.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{item.item_code} has been deleted')
        return redirect ('store-product')

    context = {
        'deleted_item': item.name
    }

    return render(request, 'store/product-delete.html', context)

@login_required
def product_inventory_list(request, pk):
    items = Product.objects.get(id=pk) #get the id's name/models
    stocks = FinishedGoodsInventory.objects.filter(product__id = items.id) #argument refer to Product models, then double underscore needed to refer to the product's model attribute

    total = stocks.filter(stock_type = 1).aggregate(Sum('quantity'))

    context = {
        'items': items,
        'stocks': stocks,
        'total': total
    }

    return render(request, 'store/product-details.html', context)

@login_required
def product_inventory_transaction(request, pk):
    inventory = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = InventoryForm(request.POST, initial={'product': inventory})

        if form.is_valid():
            form.save()
            product_details = inventory
            messages.success(request, f"{product_details.name} ({product_details.item_code}) inventory has been updated")
            return redirect('store-product-inventory-list', inventory.id) #inventory.id will act as pk in the url of the redirect link to return after register
    else:
        form = InventoryForm(initial={'product': inventory})  


    context = {
        'inventory': inventory,
        'form': form,
    }
    return render(request, 'store/product-inventory-transaction.html', context)

@login_required
def product_inventory_update(request, pk , fk): #pk and fk will act as variable in the url slug, the values will be determine based on the arrangement and value based on the contexts passed in the href
    inventory_id = FinishedGoodsInventory.objects.get(id=pk)
    #items = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = InventoryForm(request.POST, instance = inventory_id)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            item_code = Product.objects.get(id = inventory_id.product_id).item_code
            messages.success(request, f'{inventory_id.product} ({item_code}) inventory has been updated')
            return redirect('store-product-inventory-list', inventory_id.product_id)
    else:
        form = InventoryForm(instance = inventory_id)    
    context = {
        'form': form,
        'inventory_id': inventory_id
    }

    return render(request, 'store/product-inventory-update.html', context)


@login_required
def product_inventory_delete(request, pk, fk):
    inventory_id = FinishedGoodsInventory.objects.get(id=pk)

    if request.method == 'POST':
        inventory_id.delete()
        item_code = Product.objects.get(id = inventory_id.product_id).item_code
        messages.success(request, f'{inventory_id.product} ({item_code}) inventory has been deleted')
        return redirect ('store-product-inventory-list', inventory_id.product_id)

    context = {
        'inventory_id': inventory_id
    }

    return render(request, 'store/product-inventory-delete.html', context)
