import sys
import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ...models import Glucose, Category


DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'


class Command(BaseCommand):
    args = '<filepath...> <username...>'
    help = 'Import data from a CSV file.'

    def handle(self, *args, **options):
        if len(args) != 2:
            sys.stdout.write('You must specify a filepath and username.\n')
            sys.exit(1)

        filepath = args[0]
        username = args[1]

        user = User.objects.get(username=username)

        csv_data = []
        with open(filepath, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                csv_data.append(row)

        # Assume first row is the header, so let's skip it.
        data_dict_list = self.to_dictionary(csv_data[1:])

        for i in data_dict_list:
            Glucose.objects.create(
                user=user,
                value=i['value'],
                category=i['category'],
                record_date=i['record_date'],
                record_time=i['record_time'],
                notes=i['notes']
            )

    def to_dictionary(self, data):
        """
        Convert the CSV data to a dictionary.

        This method also checks for value errors. It's less efficient than
        going through the data and creating the Glucose objects right away,
        but it lets us ensure that all the data are in the proper format
        before importing.

        Assumed order: value, category, record_date, record_time, notes
        Assume format:
            record_date = mm/dd/yyyy
            record_time = hh:mm AM/PM
        """
        data_dict_list = []
        try:
            for row in data:
                data_dict_list.append({
                    'value': int(row[0]),
                    'category': Category.objects.get(name__iexact=row[1].strip()),
                    'record_date': datetime.strptime(row[2], DATE_FORMAT),
                    'record_time': datetime.strptime(row[3], TIME_FORMAT),
                    'notes': row[4]
                })
        except ValueError, e:
            sys.stdout.write('Invalid value or format: %s\n' % e)
            sys.exit(1)

        return data_dict_list