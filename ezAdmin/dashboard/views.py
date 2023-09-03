from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product


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
        'items': items
    }

    return render(request, 'dashboard/product.html', context)
