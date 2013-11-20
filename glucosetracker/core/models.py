from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified'
    fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserSettings(TimeStampedModel):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user = models.OneToOneField(User, related_name='settings')
    time_zone = models.CharField('Time Zone', null=False, blank=False,
                                 max_length=155, default=settings.TIME_ZONE)

    glucose_high = models.PositiveIntegerField(
        'High', null=False, blank=False, default=180)
    glucose_low = models.PositiveIntegerField(
        'Low', null=False, blank=False, default=60)
    glucose_target_min = models.PositiveIntegerField(
        'Min Target', null=False,  blank=False, default=70)
    glucose_target_max = models.PositiveIntegerField(
        'Max Target', null=False, blank=False, default=120)

    class Meta:
        verbose_name_plural = 'User Settings'