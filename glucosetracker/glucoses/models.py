from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel


class Glucose(TimeStampedModel):
    user = models.ForeignKey(User)
    value = models.IntegerField() # in mg/dL
    category = models.ForeignKey('Category')
    record_date = models.DateField('Date')
    record_time = models.TimeField('Time')
    notes = models.TextField('Notes', null=False, blank=True, default='')

    def __unicode__(self):
        return str(self.value)

    class Meta:
        ordering = ['-record_date', '-record_time']


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['id']

