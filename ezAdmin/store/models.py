from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email, DecimalValidator
from django.utils import timezone
from django.db.models import Q
from misc.models import *
#from production.models import RawMaterialIdentifier
from django.apps import apps
from mixins.modify_case_fields_mixin import *


class BrandName(UppercaseFieldsMixin, models.Model):
    #basics fields
    brand_name = models.CharField(max_length = 30, unique = True)
    company_name = models.CharField(max_length = 30, blank = True, null = True)

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

class Product(UppercaseFieldsMixin, models.Model):
    identifier = models.ForeignKey('production.RawMaterialIdentifier', on_delete = models.PROTECT)
    item_code = models.CharField(max_length = 30, unique = True)
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200, blank = True, null = True)
    brand = models.ForeignKey(BrandName, on_delete = models.PROTECT)
    uom = models.ForeignKey(UOM, on_delete = models.PROTECT)
    packing = models.PositiveIntegerField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    
    #utility fields
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    exempt_fields = ['packing', 'status', 'uom', 'brand']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(Product, self).save(*args, **kwargs)

class FinishedGoodsInventory(models.Model): #change to finishedgoodinventory
    #basics fields
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    lot_number = models.CharField(max_length = 100)
    expiry_date = models.CharField(max_length = 100)
    quantity = models.PositiveIntegerField()
    stock_type = models.CharField(max_length=2,choices=(('1','Stock-in'),('2','Stock-Out')), default = 1)

    #utility fields
    stock_in_date = models.DateTimeField(blank = True, null = True)
    stock_out_date = models.DateTimeField(blank = True, null = True)
    validation_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.product.name}({self.product.item_code})'

    def save(self, *args, **kwargs):
        if self.type == '1':
            self.stock_in_date = timezone.localtime(timezone.now())
        if self.type == '2':
            self.stock_out_date = timezone.localtime(timezone.now())

        self.validation_date = timezone.localtime(timezone.now())
        super(Inventory, self).save(*args, **kwargs)
