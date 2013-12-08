from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from core.models import TimeStampedModel


class GlucoseManager(models.Manager):

    def by_user(self, user, **kwargs):
        """
        Filter objects by the 'user' field.
        """
        return self.select_related().filter(user=user)

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

    def level_breakdown(self, start_date, end_date, user):
        """
        Filter objects by glucose level and count the records for each level.

        The range for the different levels are specified in the user's
        settings.
        """
        user_settings = user.settings
        low = user_settings.glucose_low
        high = user_settings.glucose_high
        target_min = user_settings.glucose_target_min
        target_max = user_settings.glucose_target_max

        data = self.by_date(start_date, end_date, user)
        all_count = data.count()
        low_count = data.filter(value__lte=low).count()
        high_count = data.filter(value__gte=high).count()
        target_count = data.filter(
            value__gte=target_min, value__lte=target_max).count()

        result = {
            'Low': low_count,
            'High': high_count,
            'Within Target': target_count,
            'Other': all_count - (low_count + high_count + target_count)
        }

        return result

    def by_category(self, start_date, end_date, user=None):
        """
        Group objects by category and take the count.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('category__name')\
            .annotate(count=models.Count('value'))\
            .order_by('category')

    def avg_by_category(self, start_date, end_date, user=None):
        """
        Group objects by category and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('category__name')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('category')

    def avg_by_day(self, start_date, end_date, user=None):
        """
        Group objects by record date and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('record_date')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('record_date')


class Glucose(TimeStampedModel):
    objects = GlucoseManager()

    user = models.ForeignKey(User)
    value = models.PositiveIntegerField(validators=[MaxValueValidator(5000)])
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