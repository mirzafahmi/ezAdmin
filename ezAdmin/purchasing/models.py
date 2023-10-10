from django.db import models
from django.core.validators import validate_email, DecimalValidator
from dashboard.models import Product
from django.utils import timezone

class Supplier(models.Model):
    company_name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    representative_name = models.CharField(max_length=200, blank = True, null = True)
    phone_number = models.PositiveIntegerField(null = True)
    email = models.CharField(max_length = 100, validators = [validate_email], blank = True, null = True)

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.company_name}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(Supplier, self).save(*args, **kwargs)

class PurchasingDocument(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    po_number = models.CharField(max_length=200, blank = True, null = True)
    po_doc = models.FileField(upload_to='purchase_documents/PO')
    invoice_number = models.CharField(max_length=200, blank = True, null = True)
    invoice_doc = models.FileField(upload_to='purchase_documents/invoice')
    packing_list = models.CharField(max_length=200, blank = True, null = True)
    pl_doc = models.FileField(upload_to='purchase_documents/PL')
    k1_form = models.CharField(max_length=200, blank = True, null = True)
    k1_doc = models.FileField(upload_to='purchase_documents/K1')

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.po_number}({self.supplier})'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(PurchasingDocument, self).save(*args, **kwargs)

class RawMaterialIdentifier(models.Model):
    parent_item_code = models.CharField(max_length=20, unique=True)

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.parent_item_code}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(RawMaterialIdentifier, self).save(*args, **kwargs)


class RawMaterialComponent(models.Model):
    component = models.CharField(max_length=20, unique=True, blank=True, null=True)
    spec = models.CharField(max_length=200, blank = True, null = True)
    identifier = models.ForeignKey(RawMaterialIdentifier, on_delete=models.CASCADE)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material_component = models.ForeignKey(RawMaterialComponent, on_delete=models.CASCADE)
    quantity_used = models.FloatField(default=0)

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.raw_material_component} for {self.product}'
    

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(BOMComponent, self).save(*args, **kwargs)

class ProductionLog(models.Model):
    rH = models.PositiveIntegerField()
    temperature = models.PositiveIntegerField()
    BOMComponents = models.ManyToManyField(BOMComponent)
    lot_number = models.CharField(max_length=200, blank = True, null = True)
    exp_date = models.CharField(max_length=200, blank = True, null = True)

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ProductionLog, self).save(*args, **kwargs)


class RawMaterialInventory(models.Model):
    component = models.ForeignKey(RawMaterialComponent, on_delete=models.CASCADE)
    lot = models.CharField(max_length=200, blank = True, null = True)
    exp_date = models.DateTimeField()
    price_unit = models.CharField(max_length=200, blank = True, null = True)

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(RawMaterialInventory, self).save(*args, **kwargs)
