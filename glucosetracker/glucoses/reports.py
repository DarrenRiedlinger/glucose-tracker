import csv
import cStringIO
from io import BytesIO
from datetime import datetime, timedelta

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle

from django.db.models import Avg, Min, Max
from django.conf import settings
from django.core.mail import EmailMessage

from core import utils

from .models import Glucose


DATE_FORMAT = '%m/%d/%Y'
FILENAME_DATE_FORMAT = '%b%d%Y'
TIME_FORMAT = '%I:%M %p'


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
        stats = {
            'latest_entry': self.latest_entry,
            'num_records': self.data.count(),
            'hba1c': self.hba1c,
            'breakdown': self.get_breakdown(),
        }

        return stats

    @property
    def latest_entry(self):
        latest_entry = self.data.latest('id') if self.data else None

        latest_entry_value = 'None'
        latest_entry_time = latest_entry_notes = ''
        css_class = self.get_css_class(None)
        if latest_entry:
            latest_entry_value = '%s mg/dL' % latest_entry.value
            latest_entry_time = latest_entry.record_time.strftime(TIME_FORMAT)
            latest_entry_notes = latest_entry.notes
            css_class = self.get_css_class(latest_entry.value)

        return {
            'value': latest_entry_value,
            'record_time': latest_entry_time,
            'notes': latest_entry_notes,
            'css_class': css_class,
        }


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
        average = utils.round_value(
            subset.aggregate(Avg('value'))['value__avg'])
        hba1c = utils.round_value(utils.calc_hba1c(average))

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
        average = utils.round_value(
            subset.aggregate(Avg('value'))['value__avg'])
        
        highs = subset.filter(value__gt=self.user_settings['high']).count()
        lows = subset.filter(value__lt=self.user_settings['low']).count()
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
                'value': '%s mg/dL' % average if average else 'None',
                'css_class': self.get_css_class(average)
            },
            'highs': '%s (%s%%)' % (highs, utils.percent(highs, total)),
            'lows': '%s (%s%%)' % (lows, utils.percent(lows, total)),
            'within_target': '%s (%s%%)' % (
                within_target, utils.percent(within_target, total)),
            'other': '%s (%s%%)' % (other, utils.percent(other, total)),

        }

    def by_date(self, start, end):
        return self.data.filter(record_date__gte=start, record_date__lte=end)

    def get_css_class(self, value):
        css_class = 'text-default'

        low = self.user_settings['low']
        high = self.user_settings['high']
        target_min = self.user_settings['target_min']
        target_max = self.user_settings['target_max']

        # Only change the css_class if a value exists.
        if value:
            if value < low or value > high:
                css_class = 'text-danger'
            elif value >= target_min and value <= target_max:
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
            data['values'].append(utils.round_value(avg['avg_value']))

        return data

    @classmethod
    def get_avg_by_day(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_averages = Glucose.objects.avg_by_day(
            (now - timedelta(days=days)), now, user)

        data = {'dates': [], 'values': []}
        for avg in glucose_averages:
            data['dates'].append(avg['record_date'].strftime('%m/%d'))
            data['values'].append(utils.round_value(avg['avg_value']))

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
                    item.record_date.strftime(DATE_FORMAT),
                    item.record_time.strftime(TIME_FORMAT),
                    item.notes,
                ])

            return csv_data.getvalue()

        finally:
            csv_data.close()

    def email(self, recipient, subject='', message=''):
        email = EmailMessage(from_email=settings.CONTACTS['info_email'],
                             subject=subject, body=message, to=[recipient])

        attachment_filename = 'GlucoseData_%sto%s.csv' % \
                              (self.start_date.strftime(FILENAME_DATE_FORMAT),
                               self.end_date.strftime(FILENAME_DATE_FORMAT))

        email.attach(attachment_filename, self.generate(), 'text/csv')
        email.send()


class GlucosePdfReport(object):

    def __init__(self, start_date, end_date, user):
        self.start_date = start_date
        self.end_date = end_date
        self.user = user

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        # Width of a letter size paper
        self.max_width = 8.5 * inch
        self.left_margin = 0.7 * inch
        self.right_margin = 0.75 * inch
        self.top_margin = 0.7 * inch
        self.bottom_margin = 0.7 * inch

        self.fields = (
            ('value', 'Value'),
            ('category', 'Category'),
            ('date', 'Date'),
            ('time', 'Time'),
            ('notes', 'Notes'),
        )

    def generate(self):
        qs = Glucose.objects.by_date(
            self.start_date, self.end_date, self.user)
        qs = qs.order_by('-record_date', '-record_time')

        data = []
        for i in qs:
            value = i.value

            # Bold the text if the value is high or low based on the user's
            # settings
            low = self.user.settings.glucose_low
            high = self.user.settings.glucose_high
            if value < low or value > high:
                value = '<b>%s</b>' % value

            data.append({
                'value': self.to_paragraph(value),
                'category': i.category,
                'date': i.record_date.strftime(DATE_FORMAT),
                'time': i.record_time.strftime(TIME_FORMAT),
                'notes': self.to_paragraph(i.notes),
            })

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer,
                                pagesize=letter,
                                leftMargin=self.left_margin,
                                rightMargin=self.right_margin,
                                topMargin=self.top_margin,
                                bottomMargin=self.bottom_margin)

        styles = getSampleStyleSheet()
        styleH = styles['Heading1']

        story = []

        story.append(Paragraph('Glucose Data', styleH))
        story.append(Spacer(1, 0.25 * inch))

        converted_data = self.__convert_data(data)
        table = Table(converted_data,
                      self.get_width_from_percent([10, 20, 15, 15, 40]),
                      hAlign='LEFT')
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN',(1, 0),(0,-1), 'LEFT'),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))

        story.append(table)
        doc.build(story)

        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    def email(self, recipient, subject='', message=''):
        email = EmailMessage(from_email=settings.CONTACTS['info_email'],
                             subject=subject, body=message, to=[recipient])

        attachment_filename = 'GlucoseData_%sto%s.pdf' % \
                              (self.start_date.strftime(FILENAME_DATE_FORMAT),
                               self.end_date.strftime(FILENAME_DATE_FORMAT))

        email.attach(attachment_filename, self.generate(), 'application/pdf')
        email.send()

    def get_width_from_percent(self, values=[], max_width=None, indent=0):
        """
        Return the width values from the given percent values.
        """
        if not max_width:
            max_width = self.max_width

        width_diff = (max_width) - (indent + self.left_margin +
                                    self.right_margin)
        widths = [((width_diff * v) / 100) for v in values]

        return widths

    def to_paragraph(self, data):
            """
            Convert the data to a Paragraph object.

            Paragraph objects can be easily formatted using HTML-like tags
            and automatically wrap inside a table.

            The data is converted to a string first to prevent errors in case
            it is a 'None' value.
            """
            return Paragraph(str(data), self.styles['Left'])

    def __convert_data(self, data):
        """
        Convert the list of dictionaries to a list of list to create
        the PDF table.
        """
        # Create 2 separate lists in the same order: one for the
        # list of keys and the other for the names to display in the
        # table header.
        keys, names = zip(*[[k, n] for k, n in self.fields])
        new_data = [names]

        for d in data:
            new_data.append([d[k] for k in keys])

        return new_data