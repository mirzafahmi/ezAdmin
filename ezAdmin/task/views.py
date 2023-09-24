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
from django.db.models import Sum, F, FloatField
from django.http import JsonResponse

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
        print(request.POST)
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
def test(request):
    QuotationItemFormSet = inlineformset_factory(
            Quotation,
            QuotationItem,
            form=QuotationItemForm,
            extra=3,  # Number of empty forms to display
        )

    if request.method == 'POST':
        print(request.POST)
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

    return render(request, 'task/test.html', context)

@login_required
def ajax_quotation(request):
    print(request)
    customer_id = request.GET.get('customer_id')
    #product_id = request.GET.get('product_id')
    try:
        customer = Customer.objects.get(id = customer_id)
        #product = Product.objects.get(id = product_id)
        data = {
            'address': customer.address,
            'pic_name': customer.pic_name,   
            'phone_number': customer.phone_number,   
            'email': customer.email,
            'sales_person': customer.sales_person.name,
            #'item_code': product.item_code,
        }
        return JsonResponse(data)

    except Quotation.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'})


@login_required
def quotation_update(request, pk):
    QuotationItemFormSet = inlineformset_factory(
        Quotation,
        QuotationItem,
        form=QuotationItemForm,
        extra=3,  # Number of empty forms to display
        can_delete=True,
    )

    quotation = Quotation.objects.get(pk=pk)

    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST, instance=quotation)
        quotationitem_formset = QuotationItemFormSet(request.POST, instance=quotation)

        
        if quotation_form.is_valid() and quotationitem_formset.is_valid():
            # Save the Quotation form first
            quotation = quotation_form.save()

            # Set the quotation instance for the formset before saving
            quotationitem_formset.save()

            messages.success(request, f'{quotation} has been updated')
            return redirect('task-quotation-list')
            
        else:
            '''for form in quotationitem_formset:
                print(form.instance.id)
            #print(quotationitem_formset.instance)'''
            print(quotationitem_formset.errors)

    else:
        quotation_form = QuotationForm(instance=quotation)
        quotationitem_formset = QuotationItemFormSet(instance=quotation)


    context = {
        'quotation_form': quotation_form,
        'quotationitem_formset': quotationitem_formset,
        'quotation': quotation,
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

    quotation_total = {}
    for quotation in quotations:
        quotation_total.update({
            quotation.id: 
            QuotationItem.objects.filter(quotation_id = quotation.id).aggregate(total = Sum(F('price') * F('quantity')))['total']
        })
    
    context ={
        'quotations': quotations,
        'quotation_total': quotation_total
    }

    return render(request, 'task/quotation-list.html', context)

def order_execution_list(request):
    order_executions = OrderExecution.objects.all().select_related('quotation_id__customer_id')

    context = {
        'order_executions': order_executions
        }

    return render(request, 'task/order-execution-list.html', context)


def order_execution_add(request):
    if request.method == 'POST':
        form = OrderExecutionForm(request.POST)
        if form.is_valid():
            form.save()
            selected_quotation = form.cleaned_data.get('quotation')

        return redirect('task-list')
    
    else:
        form = OrderExecutionForm()
    
    context = {
        'form': form
    }
                
    return render(request, 'task/delivery-order.html', context)

def ajax_order_execution_add(request):
    quotation_id = request.GET.get('quotation_id')
    try:
        quotation = Quotation.objects.get(id=quotation_id)
        quotation_items = QuotationItem.objects.filter(quotation=quotation)
        # Prepare the data you want to send back as JSON
        data = {
            'quotation': {
                'customer_id': quotation.customer_id.company_name,
                'doc_number': quotation.doc_number,
                'company_address': quotation.customer_id.address,
                'pic_name': quotation.customer_id.pic_name,
                'pic_phone_number': quotation.customer_id.phone_number,
                # Add more fields as needed
            },
            'quotation_items': [
                {
                    'product': item.product.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    # Add more fields as needed
                }
                for item in quotation_items
            ],
        }
        return JsonResponse(data)

    except Quotation.DoesNotExist:
        return JsonResponse({'error': 'Quotation not found'})



def order_execution_details(request, pk):
    order = OrderExecution.objects.get(pk=pk)

    quotation = Quotation.objects.get(quotation_id = order.quotation_id)

    quotation_item = QuotationItem.object.filter(id = quotation.id)

    return render(request, 'task/delivery-order.html', context)


from django.http import JsonResponse

