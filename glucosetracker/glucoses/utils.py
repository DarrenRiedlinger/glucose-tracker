from datetime import datetime

from .models import Category


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