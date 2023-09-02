from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def posscode_validator(value):
    if len(str(value)) != 5:
        raise ValidationError(
            _('%(value)s is valid posscode'),
            params={'value': value},
        )