from datetime import datetime, date, timedelta

from django.contrib.auth.models import User

from factory import DjangoModelFactory, Sequence, SubFactory, LazyAttribute
from factory.fuzzy import FuzzyInteger, FuzzyChoice, FuzzyNaiveDateTime

from ..models import Glucose, Category


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    username = Sequence(lambda n: 'user{0}'.format(n))


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
    notes = 'This is a demo of GlucoseTracker.'




