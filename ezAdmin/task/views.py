from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from dashboard.forms import *
from task.forms import *
from django.contrib import messages
from django.forms import modelformset_factory

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
        customer_form = QuotationForm(request.POST)
        OrderFormSet = modelformset_factory(QuotationItem, QuotationItemForm, fields = {'quotation', 'product', 'quantity', 'price'})
        product_form = OrderFormSet(request.POST)
        if customer_form.is_valid and product_form.is_valid():
            customer_form.save()
            product_form.save()
            #product_name = form.cleaned_data.get('name')
            #messages.success(request, f'{product_name} has been added')
            return redirect ('task-list')
    else:
        customer_form = QuotationForm()
        OrderFormSet = modelformset_factory(QuotationItem, QuotationItemForm, fields = {'quotation', 'product', 'quantity', 'price'})
        product_form = OrderFormSet()

    context ={
        'customer_form': customer_form,
        'product_form': product_form,
    }

    return render(request, 'task/quotation.html', context)

@login_required
def quotation_details(request):
    quotations = Quotation.objects.all()

    context ={
        'quotations': quotations
    }

    return render(request, 'task/quotation-list.html', context)


@login_required
def quotation_update(request, pk):
    customer = Quotation.objects.get(id = pk)

    if request.method == 'POST':
        customer_form = QuotationForm(request.POST, instance = customer)
        product_form_set = formset_factory(QuotationItemForm)
        product_form = product_form_set(request.POST)
        if customer_form.is_valid and product_form.is_valid():
            customer_form.save()
            product_form.save()
            #product_name = form.cleaned_data.get('name')
            #messages.success(request, f'{product_name} has been added')
            return redirect ('task-list')
    else:
        customer_form = QuotationForm(instance = customer)
        product_form = QuotationItemForm()

    context ={
        'customer_form': customer_form,
        'product_form': product_form,
    }

    return render(request, 'task/quotation-update.html', context)