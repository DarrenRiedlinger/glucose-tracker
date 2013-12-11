from datetime import datetime, date, timedelta

from factory import DjangoModelFactory, Sequence, SubFactory
from factory.fuzzy import FuzzyInteger, FuzzyNaiveDateTime

from core.tests.factories import UserFactory

from ..models import Glucose, Category


class CategoryFactory(DjangoModelFactory):
    FACTORY_FOR = Category

    name = Sequence(lambda n: 'Category{0}'.format(n))


class GlucoseFactory(DjangoModelFactory):
    FACTORY_FOR = Glucose

    user = SubFactory(UserFactory)
    value = FuzzyInteger(50, 240)
    category = SubFactory(CategoryFactory)
    record_date = date.today()
    record_time = FuzzyNaiveDateTime(datetime.now() - timedelta(hours=24))
    notes = 'Hold SHIFT+Column Name to sort by multiple columns.'



