from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Inventory
from .forms import ProductForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

@login_required
def task(request):
    return render(request, 'dashboard/task.html')

@login_required
def delivery_order(request):
    return render(request, 'task/delivery_order.html')

@login_required
def invoices(request):
    return render(request, 'task/invoices.html')

@login_required
def proforma_invoices(request):
    return render(request, 'task/proforma_invoices.html')

@login_required
def product_list(request):
    items = Product.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'dashboard/product.html', context)

@login_required
def product_details(request, pk):
    items = Product.objects.get(id=pk)
    stock = Inventory
    context = {
        'items': items,
        'stock': stock
    }

    return render(request, 'dashboard/product-details.html', context)

@login_required
def product_add(request):
    items = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
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
        return redirect ('dashboard-product')

    context = {
        'deleted_item': item.name
    }

    return render(request, 'dashboard/product-delete.html', context)
