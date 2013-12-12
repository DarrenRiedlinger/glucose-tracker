import math


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calc_hba1c(value):
    """
    Calculate the HbA1c from the given average blood glucose value.

    This formula is the same one used by Accu-Chek:
    https://www.accu-chek.com/us/glucose-monitoring/a1c-calculator.html#
    """
    if value:
        return ((46.7 + value) / 28.7)
    else:
        return 0



def round_value(value):
    """
    Round the given value.

    If the value is 0 or None, then simply return 0.
    """
    if value:
       return math.ceil(value*100)/100
    else:
        return 0


def percent(part, whole):
    """
    Get the percentage of the given values.

    If the the total/whole is 0 or none, then simply return 0.
    """
    if whole:
        return round_value(100 * float(part)/float(whole))
    else:
        return 0