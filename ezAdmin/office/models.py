from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from purchasing.models import Supplier
from mixins.modify_case_fields_mixin import *

class ElectronicUserLocation(UppercaseFieldsMixin, models.Model):
    company_name = models.CharField(max_length = 100, unique = True)
    careholder_name = models.CharField(max_length = 100, unique = True)
    phone_number = models.CharField(max_length = 15, blank = True, null = True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.company_name}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicUserLocation, self).save(*args, **kwargs)

class ElectronicUser(UppercaseFieldsMixin, models.Model):
    name = models.CharField(max_length = 100, unique = True)
    position = models.CharField(max_length = 100)
    location = models.ForeignKey(ElectronicUserLocation, on_delete=models.PROTECT)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.name} ({self.position})'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicUser, self).save(*args, **kwargs)

class ElectronicBrand(UppercaseFieldsMixin, models.Model):
    brand_name = models.CharField(max_length = 100, unique = True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicBrand, self).save(*args, **kwargs)

class ElectronicModel(UppercaseFieldsMixin, models.Model):
    brand = models.ForeignKey(ElectronicBrand, on_delete=models.PROTECT)
    model_name = models.CharField(max_length = 100, unique = True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.brand} {self.model_name}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicModel, self).save(*args, **kwargs)

class ElectronicPurchasingDocument(UppercaseFieldsMixin, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete = models.PROTECT)
    po_number = models.CharField(max_length=200, blank = True, null = True)
    po_doc = models.FileField(
        upload_to='office/purchasing_documents/PO',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
        )
    invoice_number = models.CharField(max_length=200, blank = True, null = True)
    invoice_doc = models.FileField(
        upload_to='office/purchasing_documents/invoice',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    exempt_fields = []

    def __str__(self):
        return f'{self.po_number}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicPurchasingDocument, self).save(*args, **kwargs)


class ElectronicInventory(UppercaseFieldsMixin, models.Model):
    electronic_item = models.ForeignKey(ElectronicModel, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length = 100, unique = True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_purchase = models.DateField()
    purchasing_document = models.ForeignKey(ElectronicPurchasingDocument, on_delete=models.PROTECT)
    status = models.CharField(max_length=10,choices=(('Idle','Idle'),('In-Use','In-Use')), default = 'Idle')
    remark = models.CharField(max_length = 200, null=True, blank=True)
    previous_users = models.ManyToManyField(ElectronicUser, related_name='previous_users')

    exempt_fields = ['status']

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.electronic_item} (SN: {self.serial_number})'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicInventory, self).save(*args, **kwargs)

class ElectronicTransaction(models.Model):
    current_user = models.ForeignKey(ElectronicUser, on_delete=models.PROTECT)
    electronic_item = models.ForeignKey(ElectronicInventory, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20,choices=(('Checked-Out','Checked-Out'),('Checked-In','Checked-In')), default = 'Checked-Out') 
    initial_agreement_doc = models.FileField(
        upload_to='office/agreement/initial',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )
    return_agreement_doc = models.FileField(
        upload_to='office/agreement/return',
        blank=True,
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.electronic_item} ({self.current_user})'

    def save(self, *args, **kwargs):

        # Get the related ElectronicInventory
        electronic_inventory = self.electronic_item

        try:
            # Try to get the current state of the transaction
            current_transaction = ElectronicTransaction.objects.get(pk=self.pk)

            # Check if the transaction type changed
            if (
                current_transaction.transaction_type != self.transaction_type
            ):
                if self.transaction_type == 'Checked-Out':
                    electronic_inventory.status = 'In-Use'
                elif self.transaction_type == 'Checked-In':
                    electronic_inventory.status = 'Idle'

        except ElectronicTransaction.DoesNotExist:
            if self.transaction_type == 'Checked-Out':
                    electronic_inventory.status = 'In-Use'
            elif self.transaction_type == 'Checked-In':
                electronic_inventory.status = 'Idle'

        electronic_inventory.save()

        electronic_inventory.previous_users.add(self.current_user)


        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(ElectronicTransaction, self).save(*args, **kwargs)