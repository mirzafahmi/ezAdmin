from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Product, Inventory
from dashboard.forms import ProductForm, InventoryForm
from .forms import CustomerQuotationForm
from django.contrib import messages

# Create your views here.
@login_required
def task(request):
    return render(request, 'dashboard/task.html')

@login_required
def delivery_order(request):
    return render(request, 'task/delivery-order.html')

@login_required
def invoices(request):
    return render(request, 'task/invoices.html')

@login_required
def proforma_invoices(request):
    return render(request, 'task/proforma-invoices.html')
    
@login_required
def quotation(request):
    if request.method == 'POST':
        customer_form = CustomerQuotationForm(request.POST)
        inventory_form = InventoryForm(request.POST)
        if form.is_valid():
            customer_form.save()
            inventory_form.save()
            #product_name = form.cleaned_data.get('name')
            #messages.success(request, f'{product_name} has been added')
            return redirect ('task-list')
    else:
        customer_form = CustomerQuotationForm()
        inventory_form = InventoryForm()

    context ={
        'customer_form': customer_form,
        'inventory_form': inventory_form,
    }

    return render(request, 'task/quotation.html', context)