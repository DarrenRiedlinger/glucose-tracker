import csv
import cStringIO
from datetime import datetime, timedelta

from django.db.models import Avg, Min, Max
from django.conf import settings
from django.core.mail import EmailMessage

import core

from .models import Glucose


class UserStats(object):

    def __init__(self, user):
        self.user = user
        self.data = Glucose.objects.by_user(self.user)

    @property
    def user_settings(self):
        user_settings = self.user.settings
        low = user_settings.glucose_low
        high = user_settings.glucose_high
        target_min = user_settings.glucose_target_min
        target_max = user_settings.glucose_target_max

        return {
            'low': low,
            'high': high,
            'target_min': target_min,
            'target_max': target_max
        }

    @property
    def user_stats(self):
        latest_entry_value = self.data.latest('id').value \
            if self.data else None
        latest_entry = {
            'value': '%s mg/dL' % latest_entry_value \
                if latest_entry_value else 'None',
            'css_class': self.get_css_class(latest_entry_value),
        }

        num_records = self.data.count()

        stats = {
            'latest_entry': latest_entry,
            'num_records': num_records,
            'hba1c': self.hba1c,
            'breakdown': self.get_breakdown(),
        }

        return stats

    @property
    def hba1c(self):
        """
        The HbA1c is calculated using the average blood glucose from the last
        90 days.

            Less than 7 = Excellent
            Between 7 and 8 = Average
            Greater than 8 = Bad
        """
        now = datetime.now(tz=self.user.settings.time_zone).date()
        subset = self.by_date(now - timedelta(days=90), now)
        average = core.utils.round_value(
            subset.aggregate(Avg('value'))['value__avg'])
        hba1c = core.utils.round_value(core.utils.calc_hba1c(average))

        css_class = 'text-default'

        if hba1c:
            if hba1c < 7:
                css_class = 'text-success'
            elif hba1c > 8:
                css_class = 'text-danger'
            else:
                css_class = 'text-primary'

        value_html = '%s%%<br><small>(%s mg/dL)</small>' % (hba1c, average) \
            if hba1c else 'None<br><small>(None)</small>'

        return {
            'value': value_html,
            'css_class': css_class
        }

    def get_breakdown(self, days=14):
        now = datetime.now(tz=self.user.settings.time_zone).date()
        subset = self.by_date(now - timedelta(days=days), now)

        total = subset.count()
        lowest = subset.aggregate(Min('value'))['value__min']
        highest = subset.aggregate(Max('value'))['value__max']
        average = core.utils.round_value(
            subset.aggregate(Avg('value'))['value__avg'])
        
        highs = subset.filter(value__gte=self.user_settings['high']).count()
        lows = subset.filter(value__lte=self.user_settings['low']).count()
        within_target = subset.filter(
            value__gte=self.user_settings['target_min'],
            value__lte=self.user_settings['target_max']
        ).count()
        other = total - (highs + lows + within_target)

        return {
            'total': total,
            'lowest': {
                'value': '%s mg/dL' % lowest if lowest else 'None',
                'css_class': self.get_css_class(lowest),
            },
            'highest': {
                'value': '%s mg/dL' % highest if highest else 'None',
                'css_class': self.get_css_class(highest),
            },  
            'average': {
                'value': average,
                'css_class': self.get_css_class(average)
            },
            'highs': '%s (%s%%)' % (highs, core.utils.percent(highs, total)),
            'lows': '%s (%s%%)' % (lows, core.utils.percent(lows, total)),
            'within_target': '%s (%s%%)' % (
                within_target, core.utils.percent(within_target, total)),
            'other': '%s (%s%%)' % (other, core.utils.percent(other, total)),

        }

    def by_date(self, start, end):
        return self.data.filter(record_date__gte=start, record_date__lte=end)

    def get_css_class(self, value):
        css_class = 'text-default'

        # Only change the css_class if a value exists.
        if value:
            if value < self.user_settings['low'] \
                or value > self.user_settings['high']:
                css_class = 'text-danger'
            elif value >= self.user_settings['target_min'] \
                and value <= self.user_settings['target_max']:
                css_class = 'text-success'
            else:
                css_class = 'text-primary'

        return css_class


class ChartData(object):

    @classmethod
    def get_count_by_category(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        category_count = Glucose.objects.by_category(
            (now - timedelta(days=days)), now, user)

        data = [[c['category__name'], c['count']] for c in category_count]

        return data

    @classmethod
    def get_level_breakdown(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_level = Glucose.objects.level_breakdown(
            (now - timedelta(days=days)), now, user)

        chart_colors = {
            'Low': 'orange',
            'High': 'red',
            'Within Target': 'green',
            'Other': 'blue'
        }

        data = []
        keyorder = ['Low', 'High', 'Within Target', 'Other']
        for k, v in sorted(glucose_level.items(),
                           key=lambda i: keyorder.index(i[0])):
            data.append({'name': k, 'y': v, 'color': chart_colors[k]})

        return data

    @classmethod
    def get_avg_by_category(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()
        
        glucose_averages = Glucose.objects.avg_by_category(
            (now - timedelta(days=days)), now, user)

        data = {'categories': [], 'values': []}
        for avg in glucose_averages:
            data['categories'].append(avg['category__name'])
            data['values'].append(core.utils.round_value(avg['avg_value']))

        return data

    @classmethod
    def get_avg_by_day(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_averages = Glucose.objects.avg_by_day(
            (now - timedelta(days=days)), now, user)

        data = {'dates': [], 'values': []}
        for avg in glucose_averages:
            data['dates'].append(avg['record_date'].strftime('%m/%d'))
            data['values'].append(core.utils.round_value(avg['avg_value']))

        return data


class GlucoseCsvReport(object):

    def __init__(self, start_date, end_date, user):
        self.start_date = start_date
        self.end_date = end_date
        self.user = user

    def generate(self):
        data = Glucose.objects.by_date(
            self.start_date, self.end_date, self.user)
        data = data.order_by('-record_date', '-record_time')

        csv_data = cStringIO.StringIO()
        try:
            writer = csv.writer(csv_data)
            writer.writerow(['Value', 'Category', 'Date', 'Time', 'Notes'])

            for item in data:
                writer.writerow([
                    item.value,
                    item.category,
                    item.record_date.strftime('%m/%d/%Y'),
                    item.record_time.strftime('%I:%M %p'),
                    item.notes,
                ])

            return csv_data.getvalue()

        finally:
            csv_data.close()

    def email(self, recipient, subject='', message=''):
        email = EmailMessage(from_email=settings.CONTACTS['info_email'],
                             subject=subject, body=message, to=[recipient])

        attachment_filename = 'GlucoseData_%sto%s.csv' % \
                              (self.start_date.strftime('%b%d%Y'),
                               self.end_date.strftime('%b%d%Y'))

        email.attach(attachment_filename, self.generate(), 'text/csv')
        email.send()