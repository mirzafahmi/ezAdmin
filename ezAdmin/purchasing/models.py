from django.db import models
from django.core.validators import validate_email, DecimalValidator
from django.utils import timezone
from django.contrib.auth.models import User

from mixins.modify_case_fields_mixin import CapitalcaseFieldsMixin, UppercaseFieldsMixin
from misc.models import Currency


class Supplier(UppercaseFieldsMixin, models.Model):
    company_name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    representative_name = models.CharField(max_length=200, blank = True, null = True)
    phone_number = models.CharField(max_length = 15, blank = True, null = True)
    email = models.CharField(max_length = 100, validators = [validate_email], blank = True, null = True)
    currency_trade = models.ForeignKey(Currency, on_delete=models.PROTECT)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    exempt_fields = ['email']

    def __str__(self):
        return f'{self.company_name}'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())

        super(Supplier, self).save(*args, **kwargs)

class PurchasingDocument(UppercaseFieldsMixin, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete = models.PROTECT)
    po_number = models.CharField(max_length=200, blank = True, null = True)
    po_doc = models.FileField(
        upload_to='purchasing_documents/PO',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )
    invoice_number = models.CharField(max_length=200, blank = True, null = True)
    invoice_doc = models.FileField(
        upload_to='purchasing_documents/invoice',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )
    packing_list = models.CharField(max_length=200, blank = True, null = True)
    pl_doc = models.FileField(
        upload_to='purchasing_documents/PL',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )
    k1_form = models.CharField(max_length=200, blank = True, null = True)
    k1_doc = models.FileField(
        upload_to='purchasing_documents/K1',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )
    k1_form_rate = models.FloatField()
    AWB_number = models.CharField(max_length=200, blank = True, null = True)
    AWB_doc = models.FileField(
        upload_to='purchasing_documents/AWB',
        help_text='Maximum file size: 5 MB. Allowed extensions: .pdf',
    )

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.po_number}({self.supplier})'

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        
        super(PurchasingDocument, self).save(*args, **kwargs)
