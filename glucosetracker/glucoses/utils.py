from datetime import datetime

from .models import Category, Glucose


def get_initial_category(time_zone):
    now = datetime.now(tz=time_zone)

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

    return Category.objects.get(name=category_name)