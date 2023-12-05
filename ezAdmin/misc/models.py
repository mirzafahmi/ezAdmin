from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email, DecimalValidator
from django.utils import timezone
from django.db.models import Q
from mixins.modify_case_fields_mixin import *

class Currency(models.Model):
    name = models.CharField(max_length = 20, unique = True)
    currency_code = models.CharField(max_length = 3, unique = True)

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
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
    name = models.CharField(max_length = 10, unique = True)
    unit = models.CharField(max_length = 10)
    weightage = models.FloatField()

    create_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'{self.name} ({self.unit})' 

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        super(UOM, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'UOM'
