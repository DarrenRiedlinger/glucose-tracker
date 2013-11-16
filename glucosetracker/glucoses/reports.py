import csv
import cStringIO

from django.conf import settings
from django.core.mail import EmailMessage

from .models import Glucose


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