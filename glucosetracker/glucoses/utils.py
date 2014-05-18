import csv
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Glucose


DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'


def import_glucose_from_csv(user, csv_file):
    """
    Import glucose CSV data.

    Assumed order: value, category, record_date, record_time, notes
    """
    csv_data = []
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        csv_data.append(row)

    # Assume first row is the header, so let's skip it.
    for row in csv_data[1:]:
        try:
            category = Category.objects.get(name__iexact=row[1].strip())
        except ObjectDoesNotExist:
            category = Category.objects.get(
                name__iexact='No Category'.strip())
        Glucose.objects.create(
            user=user,
            value=int(row[0]),
            category=category,
            record_date=datetime.strptime(row[2], DATE_FORMAT),
            record_time=datetime.strptime(row[3], TIME_FORMAT),
            notes=row[4],
        )


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