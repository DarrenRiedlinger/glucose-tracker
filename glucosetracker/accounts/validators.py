from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email=value)

    if exists:
        raise ValidationError('Someone is already using this email address. '
                              'Please try another.')

def validate_username_unique(value):
    exists = User.objects.filter(username=value)

    if exists:
        raise ValidationError('This username is not available. '
                              'Please try another.')