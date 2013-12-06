import math
import csv
import cStringIO
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMessage

from .models import Glucose


class ChartData(object):

    @classmethod
    def get_levels_breakdown(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_levels = Glucose.objects.levels_breakdown(
            (now - timedelta(days=days)), now, user)

        chart_colors = {
            'Low': 'orange',
            'High': 'red',
            'Within Target': 'green',
            'Other': 'blue'
        }

        data = []
        for k, v in glucose_levels.iteritems():
            data.append({'name': k, 'y': v, 'color': chart_colors[k]})

        return {'data': data}

    @classmethod
    def get_avg_by_category(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()
        
        glucose_averages = Glucose.objects.avg_by_category(
            (now - timedelta(days=days)), now, user)

        data = {'categories': [], 'values': []}
        for avg in glucose_averages:
            data['categories'].append(avg['category__name'])
            data['values'].append(math.ceil(avg['avg_value']*100)/100)

        return data

    @classmethod
    def get_avg_by_day(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_averages = Glucose.objects.avg_by_day(
            (now - timedelta(days=days)), now, user)

        data = {'dates': [], 'values': []}
        for avg in glucose_averages:
            data['dates'].append(avg['record_date'].strftime('%m/%d'))
            data['values'].append(math.ceil(avg['avg_value']*100)/100)

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