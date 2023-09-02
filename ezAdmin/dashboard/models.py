from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email, DecimalValidator
import sys
sys.path.insert(0, '/ezAdmin/validator')
from validator.posscode import posscode_validator
from validator.abbreaviation import create_acronym as abv

# Create your models here.
BRAND = (
    ('ProDetect', 'ProDetect'),
    ('GenoAmp', 'GenoAmp'),
    ('Wondfo', 'Wondfo'),
    ('Finecare', 'Finecare'),
    ('Sejoy', 'Sejoy')
)

class BrandName(models.Model):
    brand_name = models.CharField(max_length = 20, unique = True)
    create_date = models.DateTimeField(auto_now_add = True)

class SalesPerson(models.Model):
    name = models.CharField(max_length = 100)
    #name_abv = abv(name)
    create_date = models.DateTimeField(auto_now_add = True)

class Currency(models.Model):
    name = models.CharField(max_length = 20, null = True)

class UOM(models.Model):
    name = models.CharField(max_length = 5, unique = True)

    class Meta:
        verbose_name_plural = 'UOM'

class Product(models.Model):
    item_code = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)
    brand = models.ForeignKey(BrandName, on_delete = models.CASCADE)
    uom = models.ForeignKey(UOM, on_delete = models.CASCADE)
    packing = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

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

class DeliveryMethod(models.Model):
    name = models.CharField(max_length = 100)
    payment_term = models.CharField(max_length = 100)
    representative = models.CharField(max_length = 20)
    price_KG = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

class Inquiry(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    doc_number = models.CharField(max_length = 100)
    price_per_unit = models.PositiveIntegerField(validators = [DecimalValidator(99999,2)])
    quantity = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

class OrderExecution:
    inquiry_id = models.ForeignKey(Inquiry, on_delete = models.CASCADE)
    doc_number = models.PositiveIntegerField(validators = [DecimalValidator(6,0)])
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete = models.CASCADE)
    tracking_number = models.CharField(max_length = 100)
    create_date = models.DateTimeField(auto_now_add = True)