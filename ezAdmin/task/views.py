from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from dashboard.forms import *
from task.forms import *
from django.contrib import messages
from django.forms import inlineformset_factory, formset_factory
from django.views.generic import (TemplateView, ListView, CreateView, DetailView, DeleteView, FormView)
from django.views.generic.detail import SingleObjectMixin

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
    QuotationItemFormSet = inlineformset_factory(
            Quotation,
            QuotationItem,
            form=QuotationItemForm,
            extra=3,  # Number of empty forms to display
        )

    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST)
        quotationitem_formset = QuotationItemFormSet(request.POST)

        if quotation_form.is_valid() and quotationitem_formset.is_valid():
            # Save the Quotation form first
            quotation = quotation_form.save()

            # Iterate through the QuotationItem forms and associate them with the saved Quotation
            for quotationitem_form in quotationitem_formset:
                if quotationitem_form.cleaned_data:
                    quotationitem = quotationitem_form.save(commit=False)
                    quotationitem.quotation = quotation
                    quotationitem.save()

            messages.success(request, f'{quotation} has been created')
            return redirect('task-quotation-list')
    else:
        quotation_form = QuotationForm()
        quotationitem_formset = QuotationItemFormSet(queryset=QuotationItem.objects.none())


    context ={
        'quotation_form': quotation_form,
        'quotationitem_formset': quotationitem_formset,
    }

    return render(request, 'task/quotation.html', context)

@login_required
def quotation_update(request, pk):
    QuotationItemFormSet = inlineformset_factory(
            Quotation,
            QuotationItem,
            form=QuotationItemForm,
            extra=3,  # Number of empty forms to display
            can_delete = True,
        )

    quotation = Quotation.objects.get(pk = pk)
    quotation_form = QuotationForm(instance=quotation)
    quotationitem_formset = QuotationItemFormSet(instance=quotation)
    
    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST, instance=quotation)
        quotationitem_formset = QuotationItemFormSet(request.POST, instance=quotation)
        
        if quotation_form.is_valid() and quotationitem_formset.is_valid():
            quotation_form.save()
            quotationitem_formset.save()

            messages.success(request, f'{quotation} has been updated')
            return redirect('task-quotation-list')

    context ={
        'quotation_form': quotation_form,
        'quotationitem_formset': quotationitem_formset,
        'quotation': quotation
    }
    
    return render(request, 'task/quotation-update.html', context)

@login_required
def quotation_delete(request, pk):
    quotation = Quotation.objects.get(pk = pk)

    if request.method == 'POST':
        quotation.delete()
        messages.success(request, f'{quotation} has been deleted')

        return redirect('task-quotation-list')

    context = {
        'quotation': quotation
    }

    return render(request, 'task/quotation-delete.html', context)

@login_required
def quotation_details(request):
    quotations = Quotation.objects.all()

    context ={
        'quotations': quotations
    }

    return render(request, 'task/quotation-list.html', context)

