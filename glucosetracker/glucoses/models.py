from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from core.models import TimeStampedModel


class GlucoseManager(models.Manager):

    def by_user(self, user, **kwargs):
        """
        Filter objects by the 'user' field.
        """
        return self.select_related().filter(user=user)

    def avg_by_category(self, start_date, end_date, user=None, **kwargs):
        """
        Group objects by category and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('category__name')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('category')

    def avg_by_day(self, start_date, end_date, user=None, **kwargs):
        """
        Group objects by record date and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('record_date')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('record_date')

    def by_date(self, start_date, end_date, user=None, **kwargs):
        """
        Filter objects by date range.
        """
        if user:
            resultset = self.select_related().filter(
                user=user,
                record_date__gte=start_date,
                record_date__lte=end_date)
        else:
            resultset = self.select_related().filter(
                record_date__gte=start_date,
                record_date__lte=end_date)

        return resultset.order_by('-record_date', '-record_time')


class Glucose(TimeStampedModel):
    objects = GlucoseManager()

    user = models.ForeignKey(User)
    value = models.PositiveIntegerField() # in mg/dL
    category = models.ForeignKey('Category')
    record_date = models.DateField('Date')
    record_time = models.TimeField('Time')
    notes = models.TextField('Notes', null=False, blank=True, default='')
    tags = TaggableManager(blank=True, help_text=None)

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