from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email, DecimalValidator

import sys
sys.path.insert(0, '/ezAdmin/validator')
from validator.posscode import posscode_validator
from validator.abbreaviation import create_acronym as abv

# Create your models here.

class BrandName(models.Model):
    brand_name = models.CharField(max_length = 20, unique = True)
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.brand_name

class SalesPerson(models.Model):
    name = models.CharField(max_length = 100)
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    def name_abv(self):
        return abv(self.name)

class Currency(models.Model):
    name = models.CharField(max_length = 20, unique = True)
    #currency_code = models.CharField(max_length = 3, unique = True)

    def __str__(self):
        return self.name

class UOM(models.Model):
    name = models.CharField(max_length = 5, unique = True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'UOM'

class Product(models.Model):
    item_code = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)
    brand = models.ForeignKey(BrandName, on_delete = models.CASCADE)
    uom = models.ForeignKey(UOM, on_delete = models.CASCADE)
    packing = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    stock_up_date = models.DateTimeField(auto_now_add = True)

class Customer(models.Model):
    customer_id = models.CharField(max_length = 5, unique = True)
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    posscode = models.PositiveIntegerField(validators = [posscode_validator])
    email = models.CharField(max_length = 100, validators = [validate_email])
    phone_number = models.CharField(max_length = 100)
    sales_person = models.ForeignKey(SalesPerson, on_delete = models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE, null = True)
    create_date = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name

class DeliveryMethod(models.Model):
    name = models.CharField(max_length = 100)
    payment_term = models.CharField(max_length = 100)
    representative = models.CharField(max_length = 20)
    price_KG = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    doc_number =  f'QT-{SalesPerson.name_abv}{models.ForeignKey(SalesPerson, on_delete = models.CASCADE)}'
    price_per_unit = models.PositiveIntegerField(validators = [DecimalValidator(99999,2)])
    quantity = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.doc_number
class OrderExecution:
    inquiry_id = models.ForeignKey(Inquiry.doc_number, on_delete = models.CASCADE)
    do_number = f'DO-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    inv_number = f'I-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete = models.CASCADE)
    tracking_number = models.CharField(max_length = 100)
    create_date = models.DateTimeField(auto_now_add = True)