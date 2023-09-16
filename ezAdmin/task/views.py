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

            return redirect('task-quotation-list')
    else:
        quotation_form = QuotationForm()
        quotationitem_formset = QuotationItemFormSet(queryset=QuotationItem.objects.none())


    context ={
        'quotation_form': quotation_form,
        'quotationitem_formset': quotationitem_formset,
    }

    return render(request, 'task/quotation.html', context)

class QuotationUpdate(SingleObjectMixin, FormView):
    model = Quotation
    template = 'quotation-update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = Quotation.object.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = Quotation.object.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return QuotationListFormSet(**self.get_form_kwargs(), instance = self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            message.SUCCESS,
            'Changes in quotation were saved'
        )

        return render(self.request, 'task/quotation-list.html')


@login_required
def quotation_details(request):
    quotations = Quotation.objects.all()

    context ={
        'quotations': quotations
    }

    return render(request, 'task/quotation-list.html', context)


'''@login_required
def quotation_update(request, pk):
    customer = Quotation.objects.get(id = pk)
    item = QuotationItem.objects.get(quotation_id = pk)
    print(item)
    if request.method == 'POST':
        product_form = QuotationListFormSet(request.POST, instance = item)
        print(product_form)
        if product_form.is_valid():
            product_form.save()
            #product_name = form.cleaned_data.get('name')
            #messages.success(request, f'{product_name} has been added')
            return redirect ('task-list')
    else:
        product_form = QuotationListFormSet(request.POST, instance = item)
        print(product_form)

    context ={
        'customer': customer,
        'product_form': product_form,
    }

    return render(request, 'task/quotation-update.html', context)'''


'''@login_required
def quotation(request):
    if request.method == 'POST':
        form = QuotationItemForm2(request.POST)
        if form.is_valid():
            quotation = Quotation.objects.create(customer_id=form.cleaned_data['customer_id'])
            quotation_item = form.save(commit=False)
            quotation_item.customer_id = quotation
            quotation_item.save()
            return redirect('task-quotation-list')
    else:
        form = QuotationItemForm2()

    context = {
        'form': form,
    }

    return render(request, 'task/quotation.html', context)

@login_required
def quotation_item(request):
    print(instance)
    if request.method == 'POST':
        form = QuotationItemForm2(request.POST)
        if form.is_valid():
            quotation = Quotation.objects.create(customer_id=form.cleaned_data['customer_id'])
            quotation_item = form.save(commit=False)
            quotation_item.customer_id = quotation
            quotation_item.save()
            return redirect('task-quotation-list')
    else:
        form = QuotationItemForm2()

    context = {
        'form': form,
    }

    return render(request, 'task/quotation.html', context)'''