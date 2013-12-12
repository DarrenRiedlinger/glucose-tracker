import math


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def round_value(value):
    """
    Round the given value.

    If the value is 0 or None, then simply return 0.
    """
    if value:
        value = math.ceil(value*100)/100
    else:
        value = 0

    return value


def percent(part, whole):
    """
    Get the percentage of the given values.

    If the the total/whole is 0 or none, then simply return 0.
    """
    if whole:
        return round_value(100 * float(part)/float(whole))
    else:
        return 0