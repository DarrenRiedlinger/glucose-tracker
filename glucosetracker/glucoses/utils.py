import csv
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Glucose


DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'


def import_glucose_from_csv(user, csv_file):
    """
    Import glucose CSV data.

    We'll process all rows first and create Glucose model objects from them
    and perform a bulk create. This way, no records will be inserted unless
    all records are good.

    Assumed order: value, category, record_date, record_time, notes
    """
    csv_data = []
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        csv_data.append(row)

    glucose_objects = []

    # Check if headers exists. Skip the first entry if true.
    header_check = ['value', 'category', 'date', 'time']
    first_row = [i.lower().strip() for i in csv_data[0]]
    if all(i in first_row for i in header_check):
        csv_data = csv_data[1:]

    for row in csv_data:
        # Let's do an extra check to make sure the row is not empty.
        if row:
            try:
                category = Category.objects.get(name__iexact=row[1].strip())
            except ObjectDoesNotExist:
                category = Category.objects.get(name__iexact='No Category'.strip())

            glucose_objects.append(Glucose(
                user=user,
                value=int(row[0]),
                category=category,
                record_date=datetime.strptime(row[2], DATE_FORMAT),
                record_time=datetime.strptime(row[3], TIME_FORMAT),
                notes=row[4],
            ))

    Glucose.objects.bulk_create(glucose_objects)


def get_initial_category(user):
    """
    Retrieve the default category from the user settings.

    If the default category is None (labeled as 'Auto' in the settings page),
    automatically pick the category based on time of day.
    """
    user_settings = user.settings
    default_category = user_settings.default_category

    if not default_category:
        now = datetime.now(tz=user_settings.time_zone)

        breakfast_start = now.replace(hour=4, minute=0)
        breakfast_end = now.replace(hour=11, minute=0)

        lunch_start = now.replace(hour=11, minute=0)
        lunch_end = now.replace(hour=16, minute=0)

        dinner_start = now.replace(hour=16, minute=0)
        dinner_end = now.replace(hour=22, minute=0)

        if now > breakfast_start and now < breakfast_end:
            category_name = 'Breakfast'
        elif now > lunch_start and now < lunch_end:
            category_name = 'Lunch'
        elif now > dinner_start and now < dinner_end:
            category_name = 'Dinner'
        else:
            category_name = 'Bedtime'

        default_category = Category.objects.get(name=category_name)

    return default_category