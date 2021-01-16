from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_alphabetic(value):
    if bool(re.search('[^a-zA-Z]', value)) or len(value) > 1:
        raise ValidationError(
            _('%(value)s is not a single letter from a-z'),
            params={'value': value},
        )
    return value