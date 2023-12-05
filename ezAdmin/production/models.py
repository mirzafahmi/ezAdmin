from django.db import models
from django.core.validators import validate_email, DecimalValidator
from store.models import Product
from purchasing.models import *
from misc.models import *
from django.utils import timezone
from mixins.modify_case_fields_mixin import *


class RawMaterialIdentifier(UppercaseFieldsMixin, models.Model):
    parent_item_code = models.CharField(max_length=30, unique=True)
    #add description of identifier

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.parent_item_code}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(RawMaterialIdentifier, self).save(*args, **kwargs)

class RawMaterialComponent(UppercaseFieldsMixin, models.Model):
    component = models.CharField(max_length=200, blank=True, null=True)
    spec = models.CharField(max_length=200, blank = True, null = True)
    identifier = models.ForeignKey(RawMaterialIdentifier, on_delete=models.PROTECT)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.component} for {self.identifier}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(RawMaterialComponent, self).save(*args, **kwargs)
    
class BOMComponent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    raw_material_component = models.ForeignKey(RawMaterialComponent, on_delete=models.PROTECT)
    quantity_used = models.FloatField()
    uom = models.ForeignKey(UOM, on_delete=models.PROTECT)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.raw_material_component}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(BOMComponent, self).save(*args, **kwargs)

class ProductionLog(models.Model):
    rH = models.FloatField()
    temperature = models.FloatField()
    BOMComponents = models.ManyToManyField(BOMComponent)
    quantity_produced = models.PositiveIntegerField()
    lot_number = models.CharField(max_length=200, blank = True, null = True)
    exp_date = models.CharField(max_length=200, blank = True, null = True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.BOMComponents.all()[0].product.item_code} ({self.lot_number})'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ProductionLog, self).save(*args, **kwargs)

class RawMaterialInventory(CapitalcaseFieldsMixin, models.Model):
    component = models.ForeignKey(RawMaterialComponent, on_delete=models.PROTECT)
    quantity = models.FloatField()
    uom = models.ForeignKey(UOM, on_delete=models.PROTECT)
    lot_number = models.CharField(max_length=200, blank = True, null = True)
    exp_date = models.CharField(max_length=200, blank = True, null = True)
    price_per_unit = models.FloatField()
    stock_type = models.CharField(max_length=2,choices=(('1','Stock-in'),('2','Stock-Out')), default = 1)
    purchasing_doc = models.ForeignKey(PurchasingDocument, on_delete=models.PROTECT)
    stock_in_tag = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='stock_in_tag_entries')
    production_log = models.ForeignKey(ProductionLog, on_delete=models.SET_NULL, blank=True, null=True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)
    stock_in_date = models.DateTimeField(blank = True, null = True)
    stock_out_date = models.DateTimeField(blank = True, null = True)
    validation_date = models.DateTimeField(blank = True, null = True)
    

    exempt_fields = ['lot_number']

    def __str__(self):
        return f'{self.component} ({self.lot_number})'

    def save(self, *args, **kwargs):
        self.lot_number = self.lot_number.upper()

        # add self.stock_xx_date = None if any stock type selected or updated
        if self.stock_type == '1':
            super().save(*args, **kwargs)
            self.stock_in_tag = self

            self.stock_in_date = timezone.localtime(timezone.now())
            super().save(update_fields=['stock_in_tag'])

        if self.stock_type == '2':
            self.stock_out_date = timezone.localtime(timezone.now())
        
        if self.create_date  is None:
            self.create_date  = timezone.localtime(timezone.now())

        self.validation_date = timezone.localtime(timezone.now())
        super(RawMaterialInventory, self).save(*args, **kwargs)
