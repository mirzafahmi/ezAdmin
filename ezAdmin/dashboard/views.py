from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Inventory, Customer
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from .models import *
from django.urls import reverse_lazy, reverse

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def keep_session_alive(request):
    # Accessing the session will update its last access time
    request.session.modified = True
    return HttpResponse(status=200)

def permission_denied_view(request, exception):
    return render(request, 'dashboard/permission_denied.html', status=403)

@login_required
def product_list(request):
    items = Product.objects.all()
    stocks_total = {}
    for item in items:
        stock_in = Inventory.objects.filter(product_id = item.id).filter(type = '1').aggregate(sum = Sum('quantity'))['sum'] or 0
        stock_out = Inventory.objects.filter(product_id = item.id).filter(type = '2').aggregate(sum = Sum('quantity'))['sum'] or 0

        stocks_total.update({item.id: stock_in - stock_out})

    
    context = {
        'items': items,
        'stocks': stocks_total
    }

    return render(request, 'dashboard/product.html', context)

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
            return redirect ('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form
    }

    return render(request, 'dashboard/product-form.html', context)

@login_required
def product_update(request, pk):
    items = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance = items)
        if form.is_valid():
            form.save()
            messages.success(request, f'{items.name} ({items.item_code}) has been updated')
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance = items)    
    context = {
        'form': form
    }
    return render(request, 'dashboard/product-update.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{item.item_code} has been deleted')
        return redirect ('dashboard-product')

    context = {
        'deleted_item': item.name
    }

    return render(request, 'dashboard/product-delete.html', context)

@login_required
def product_inventory_list(request, pk):
    items = Product.objects.get(id=pk) #get the id's name/models
    stocks = Inventory.objects.filter(product__id = items.id) #argument refer to Product models, then double underscore needed to refer to the product's model attribute

    total = stocks.filter(type = 1).aggregate(Sum('quantity'))

    context = {
        'items': items,
        'stocks': stocks,
        'total': total
    }

    return render(request, 'dashboard/product-details.html', context)

@login_required
def product_inventory_transaction(request, pk):
    inventory = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = InventoryForm(request.POST, initial={'product': inventory})

        if form.is_valid():
            form.save()
            product_details = inventory
            messages.success(request, f"{product_details.name} ({product_details.item_code}) inventory has been updated")
            return redirect('dashboard-product-inventory-list', inventory.id) #inventory.id will act as pk in the url of the redirect link to return after register
    else:
        form = InventoryForm(initial={'product': inventory})  


    context = {
        'inventory': inventory,
        'form': form,
    }
    return render(request, 'dashboard/product-inventory-transaction.html', context)

@login_required
def product_inventory_update(request, pk , fk): #pk and fk will act as variable in the url slug, the values will be determine based on the arrangement and value based on the contexts passed in the href
    inventory_id = Inventory.objects.get(id=pk)
    #items = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = InventoryForm(request.POST, instance = inventory_id)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            item_code = Product.objects.get(id = inventory_id.product_id).item_code
            messages.success(request, f'{inventory_id.product} ({item_code}) inventory has been updated')
            return redirect('dashboard-product-inventory-list', inventory_id.product_id)
    else:
        form = InventoryForm(instance = inventory_id)    
    context = {
        'form': form,
        'inventory_id': inventory_id
    }

    return render(request, 'dashboard/product-inventory-update.html', context)


@login_required
def product_inventory_delete(request, pk, fk):
    inventory_id = Inventory.objects.get(id=pk)

    if request.method == 'POST':
        inventory_id.delete()
        item_code = Product.objects.get(id = inventory_id.product_id).item_code
        messages.success(request, f'{inventory_id.product} ({item_code}) inventory has been deleted')
        return redirect ('dashboard-product-inventory-list', inventory_id.product_id)

    context = {
        'inventory_id': inventory_id
    }

    return render(request, 'dashboard/product-inventory-delete.html', context)

@login_required
def customer_list(request):
    items = Customer.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'customer/customer.html', context)

@login_required
def customer_add(request):
    items = Customer.objects.all()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            customer_name = form.cleaned_data.get('company_name')
            messages.success(request, f'{customer_name} has been added')
            return redirect ('dashboard-customer')
    else:
        form = CustomerForm()

    context = {
        'items': items,
        'form': form
    }

    return render(request, 'customer/customer-form.html', context)

@login_required
def customer_update(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"{customer.company_name}'s account has been updated")
            return redirect('dashboard-customer')
    else:
        form = CustomerForm(instance = customer)    
        
    context = {
        'form': form,
        'customer': customer
    }
    return render(request, 'customer/customer-update.html', context)


@login_required
def customer_delete(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'{customer.company_name} has been deleted')
        return redirect ('dashboard-customer')

    context = {
        'customer': customer.company_name
    }

    return render(request, 'customer/customer-delete.html', context)

class UOMListView(LoginRequiredMixin, ListView):
    model = UOM
    template_name = 'dashboard/UOM_list.html'
    context_object_name = 'UOMs'

    def get_queryset(self):

        return UOM.objects.all()

class UOMCreateView(LoginRequiredMixin, CreateView):
    model = UOM
    form_class = UOMForm
    template_name = 'dashboard/UOM_create.html'
    success_url = reverse_lazy('dashboard-misc-uom-list')

    def form_valid(self, form):
        uom_name = form.cleaned_data['name']

        messages.success(self.request, f'{uom_name} UOM created successfully!')

        return super().form_valid(form)
    
class UOMUpdateView(LoginRequiredMixin, UpdateView):
    model = UOM
    form_class = UOMForm
    template_name = 'dashboard/UOM_update.html'
    success_url = reverse_lazy('dashboard-misc-uom-list')
    context_object_name = 'UOM'

    def form_valid(self, form):
        uom_name = self.get_object().name
        
        messages.success(self.request, f'{uom_name} UOM updated successfully!')

        return super().form_valid(form)
    
class UOMDeleteView(LoginRequiredMixin, DeleteView):
    model = UOM
    template_name = 'dashboard/UOM_delete.html'
    success_url = reverse_lazy('dashboard-misc-uom-list')
    context_object_name = 'UOM'

    def delete(self, request, *args, **kwargs):

        uom_name = self.get_object().name
        
        messages.success(self.request, f'{uom_name} UOM deleted successfully!')

        return super().delete(request *args, **kwargs)

class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = 'dashboard/currency_list.html'
    context_object_name = 'currencies'

class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'dashboard/currency_create.html'
    success_url = reverse_lazy('dashboard-misc-currency-list')

    def form_valid(self, form):
        currency = form.cleaned_data['name']
        currency_code = form.cleaned_data['currency_code']

        messages.success(self.request, f'{currency}({currency_code}) currency created successfully!')

        return super().form_valid(form)

class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'dashboard/currency_update.html'
    success_url = reverse_lazy('dashboard-misc-currency-list')
    context_object_name = 'currency'

    def form_valid(self, form):
        currency = self.get_object()

        messages.success(self.request, f'{currency.name}({currency.currency_code}) currency updated successfully!')

        return super().form_valid(form)

class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Currency
    template_name = 'dashboard/currency_delete.html'
    success_url = reverse_lazy('dashboard-misc-currency-list')
    context_object_name = 'currency'
    
    def post(self, request, *args, **kwargs):
        currency = self.get_object()
        success_message = f'{currency.name}({currency.currency_code}) currency deleted successfully!'
        messages.success(self.request, success_message)

        return super().post(request, *args, **kwargs)
    
