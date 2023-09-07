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
    currency_code = models.CharField(max_length = 3, unique = True)

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
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length = 100)
    expiry_date = models.CharField(max_length = 100)
    quantity = models.PositiveIntegerField()
    type = models.CharField(max_length=2,choices=(('1','Stock-in'),('2','Stock-Out')), default = 1)
    stock_in_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.product.name}({self.product.item_code})'

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

class Quotation(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    doc_number =  f'QT-{SalesPerson.name_abv}{models.ForeignKey(SalesPerson, on_delete = models.CASCADE)}'
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.doc_number

class Quotation_Item(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank= True, null= True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

class OrderExecution:
    quotation_id = models.ForeignKey(Quotation.doc_number, on_delete = models.CASCADE, null = True)
    do_number = f'DO-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    inv_number = f'I-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete = models.CASCADE)
    tracking_number = models.CharField(max_length = 100)
    create_date = models.DateTimeField(auto_now_add = True)