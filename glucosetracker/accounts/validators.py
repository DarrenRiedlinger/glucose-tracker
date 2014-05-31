from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email__iexact=value)

    if exists:
        raise ValidationError('Someone is already using this email address. '
                              'Please try another.')


def validate_username_unique(value):
    exists = User.objects.filter(username__iexact=value)
    invalid_usernames = [
        'glucosetracker',
        'glucose',
        'diabetes',
        'admin',
        'help',
        'helpdesk',
        'sales',
        'support',
        'info',
        'warning',
        'success',
        'danger',
        'error',
        'debug',
        'alert',
        'alerts',
        'signup',
        'signin',
        'signout',
        'login',
        'logout',
        'activate',
        'register',
        'password',
    ]

    if exists or value in invalid_usernames:
        raise ValidationError('This username is not available. '
                              'Please try another.')