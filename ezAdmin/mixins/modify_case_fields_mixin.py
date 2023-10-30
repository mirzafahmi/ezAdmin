from django.db import models

class CapitalcaseFieldsMixin(models.Model):
    exempt_fields = []

    def capitalize_words(self, value):
        # Split the string into words, capitalize each word, and join them back
        return ' '.join(word.capitalize() for word in value.split())

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.CharField):
                field_name = field.name
                if field_name not in self.exempt_fields:
                    value = getattr(self, field_name)
                    if value:
                        capitalized_value = self.capitalize_words(value)
                        setattr(self, field_name, capitalized_value)
        super(CapitalcaseFieldsMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class UppercaseFieldsMixin(models.Model):
    exempt_fields = []

    def uppercase_words(self, value):
        # Split the string into words, capitalize each word, and join them back
        return ' '.join(word.upper() for word in value.split())

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.CharField):
                field_name = field.name
                if field_name not in self.exempt_fields:
                    value = getattr(self, field_name)
                    if value:
                        uppercase_value = self.uppercase_words(value)
                        setattr(self, field_name, uppercase_value)
        super(UppercaseFieldsMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True