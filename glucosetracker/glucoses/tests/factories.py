from datetime import datetime, date, timedelta

from factory import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyChoice, FuzzyNaiveDateTime

from ..models import Glucose, Category


class GlucoseFactory(DjangoModelFactory):
    FACTORY_FOR = Glucose

    value = FuzzyInteger(50, 240)
    category = FuzzyChoice(Category.objects.all())
    record_date = date.today()
    record_time = FuzzyNaiveDateTime(datetime.now() - timedelta(hours=24))
    notes = 'GlucoseTracker.net is the best app ever made.'

    @classmethod
    def get_date_list(cls, start, end):
        delta = end - start
        return [(start + timedelta(days=i)) for i in range(delta.days+1)]




