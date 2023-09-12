from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email, DecimalValidator
from django.utils import timezone

import sys
sys.path.insert(0, '/ezAdmin/validator')
from validator.posscode import posscode_validator
from validator.abbreaviation import create_acronym as abv

# Create your models here.

class BrandName(models.Model):
    #basics fields
    brand_name = models.CharField(max_length = 20, unique = True)
    company_name = models.CharField(max_length = 20, blank = True, null = True)

    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(BrandName, self).save(*args, **kwargs)

class SalesPerson(models.Model):
    #basics fields
    name = models.CharField(max_length = 100)
    name_acronym = models.CharField(max_length = 100, blank = True, null = True)
    region = models.CharField(max_length = 20, blank = True, null = True)

    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.name_acronym = abv(str(self.name))
        self.update_date = timezone.localtime(timezone.now())
        super(SalesPerson, self).save(*args, **kwargs)

    def name_abv(self):
        return self.name

class Currency(models.Model):
    #basics fields
    name = models.CharField(max_length = 20, unique = True)
    currency_code = models.CharField(max_length = 3, unique = True)

    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(Currency, self).save(*args, **kwargs)


class UOM(models.Model):
    #basics fields
    name = models.CharField(max_length = 5, unique = True)

    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(UOM, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'UOM'

class Product(models.Model):
    #basics fields
    item_code = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 200, blank = True, null = True)
    brand = models.ForeignKey(BrandName, on_delete = models.CASCADE)
    uom = models.ForeignKey(UOM, on_delete = models.CASCADE)
    packing = models.PositiveIntegerField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    
    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(Product, self).save(*args, **kwargs)

class Inventory(models.Model):
    #basics fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length = 100)
    expiry_date = models.CharField(max_length = 100)
    quantity = models.PositiveIntegerField()
    type = models.CharField(max_length=2,choices=(('1','Stock-in'),('2','Stock-Out')), default = 1)

    #utility fields
    stock_in_date = models.DateTimeField(blank = True, null = True)
    stock_out_date = models.DateTimeField(blank = True, null = True)
    validation_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.product.name}({self.product.item_code})'

    def save(self, *args, **kwargs):
        if self.type is '1':
            self.stock_in_date = timezone.localtime(timezone.now())
        if self.type is '2':
            self.stock_out_date = timezone.localtime(timezone.now())

        self.validation_date = timezone.localtime(timezone.now())
        super(Inventory, self).save(*args, **kwargs)

class Customer(models.Model):
    #basics fields
    company_name = models.CharField(max_length = 100)
    name_acronym = models.CharField(max_length = 100, blank = True, null = True)
    address = models.CharField(max_length = 100)
    posscode = models.PositiveIntegerField(validators = [posscode_validator])
    email = models.CharField(max_length = 100, validators = [validate_email])
    pic_name = models.CharField(max_length = 100, null = True)
    phone_number = models.PositiveIntegerField(null = True)
    sales_person = models.ForeignKey(SalesPerson, on_delete = models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE, null = True)
    
    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.name_acronym = abv(str(self.company_name))
        self.update_date = timezone.localtime(timezone.now())
        super(Customer, self).save(*args, **kwargs)

class DeliveryMethod(models.Model):
    #basics fields
    name = models.CharField(max_length = 100)
    payment_term = models.CharField(max_length = 100)
    representative = models.CharField(max_length = 20)
    price_KG = models.PositiveIntegerField()

    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(DeliveryMethod, self).save(*args, **kwargs)

class Quotation(models.Model):
    #basics fields
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    doc_number =  models.CharField(max_length = 20, blank= True, null= True)
    
    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.doc_number

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.doc_number = f'QT/{SalesPerson.name_acronym}/{Customer.name_acronym}/{timezone.localtime(timezone.now()).strftime("%Y"/"%m"/"%d")}'
        self.update_date = timezone.localtime(timezone.now())
        super(Quotation, self).save(*args, **kwargs)


class Quotation_Item(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank= True, null= True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

class OrderExecution:
    quotation_id = models.ForeignKey(Quotation, on_delete = models.CASCADE, null = True)
    do_number = f'DO-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    inv_number = f'I-{models.PositiveIntegerField(validators = [DecimalValidator(6,0)])}'
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete = models.CASCADE)
    tracking_number = models.CharField(max_length = 100)
    
    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(OrderExecution, self).save(*args, **kwargs)
