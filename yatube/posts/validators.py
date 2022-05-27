from django.core.exceptions import ValidationError


def validate_not_empty(value):
    if value == '':
        raise ValidationError(
            'Напишите что-нибудь, пожалуйста ^-^',
            params={'value': value},
        )
