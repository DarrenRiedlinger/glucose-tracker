from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from core.models import TimeStampedModel


class Subscriber(TimeStampedModel):
    email = models.EmailField(null=False, blank=False, unique=True)
    source_ip = models.IPAddressField(null=True, default=None)

    def send_confirmation(self):
        subject = render_to_string('subscribers/email/subject.txt')
        subject = subject.strip()
        message = render_to_string('subscribers/email/body.txt')
        send_mail(
            subject,
            message,
            from_email=settings.CONTACTS['info_email'],
            recipient_list=[self.email],
        )

    def __unicode__(self):
        return str(self.email)

    class Meta:
        ordering = ['-created',]

