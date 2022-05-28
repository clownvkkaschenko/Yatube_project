from django.core.exceptions import ValidationError


def validate_not_empty(value):
    """checking if a string is not empty."""
    if value == '':
        raise ValidationError(
            params={'value': value},
        )
