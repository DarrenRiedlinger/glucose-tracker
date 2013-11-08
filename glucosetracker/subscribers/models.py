from django.db import models

from core.models import TimeStampedModel


class Subscriber(TimeStampedModel):
    email = models.EmailField(null=False, blank=False, unique=True)
    source_ip = models.IPAddressField(null=True, default=None)

    def __unicode__(self):
        return str(self.email)

    class Meta:
        ordering = ['-created',]

