from django.contrib.auth.models import User

from factory import DjangoModelFactory, Sequence, SubFactory

from ..models import UserSettings


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    username = Sequence(lambda n: 'user{0}'.format(n))


class UserSettingsFactory(DjangoModelFactory):
    FACTORY_FOR = UserSettings

    user = SubFactory(UserFactory)



